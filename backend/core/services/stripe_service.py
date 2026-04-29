from decimal import Decimal, ROUND_HALF_UP

import stripe
from django.conf import settings
from django.db import transaction

from core.models import Booking, Payment
from core.services.ticket_service import confirm_booking_after_payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def decimal_to_paise(amount: Decimal) -> int:
    """
    Convert INR Decimal amount to paise for Stripe.
    ₹100.50 => 10050
    """
    amount = Decimal(amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(amount * 100)


def create_stripe_checkout_session(booking: Booking):
    """
    Create Stripe Checkout session for a pending booking.
    Currency: INR for India.
    """

    seats = ", ".join([seat.seat_number for seat in booking.seats.all()])
    route = booking.schedule.bus.route

    success_url = (
        f"{settings.FRONTEND_URL}/booking/success"
        f"?booking={booking.id}"
        f"&session_id={{CHECKOUT_SESSION_ID}}"
    )

    cancel_url = (
        f"{settings.FRONTEND_URL}/booking/cancel"
        f"?booking={booking.id}"
    )

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        customer_email=booking.passenger_email,
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": f"Bus Ticket - {route.origin} to {route.destination}",
                        "description": (
                            f"PNR: {getattr(booking, 'pnr_number', booking.reference_code)} | "
                            f"Seats: {seats}"
                        ),
                    },
                    "unit_amount": decimal_to_paise(booking.total_amount),
                },
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "booking_id": str(booking.id),
            "reference_code": booking.reference_code,
            "pnr_number": getattr(booking, "pnr_number", ""),
            "user_id": str(booking.user_id),
        },
    )

    Payment.objects.create(
        booking=booking,
        provider="stripe",
        amount=booking.total_amount,
        currency="inr",
        status="initiated",
        stripe_session_id=session.id,
    )

    return session


@transaction.atomic
def handle_stripe_webhook(payload: bytes, sig_header: str):
    """
    Securely handle Stripe webhook.
    This verifies Stripe signature before confirming bookings.
    """

    event = stripe.Webhook.construct_event(
        payload=payload,
        sig_header=sig_header,
        secret=settings.STRIPE_WEBHOOK_SECRET,
    )

    event_type = event["type"]
    event_data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        session = event_data
        booking_id = session.get("metadata", {}).get("booking_id")
        stripe_session_id = session.get("id")
        payment_intent_id = session.get("payment_intent", "")

        if not booking_id:
            return event

        try:
            booking = Booking.objects.select_for_update().get(id=booking_id)
        except Booking.DoesNotExist:
            return event

        payment = Payment.objects.filter(
            booking=booking,
            stripe_session_id=stripe_session_id,
        ).first()

        if payment and payment.status == "succeeded":
            return event

        if payment:
            payment.status = "succeeded"
            payment.stripe_payment_intent_id = payment_intent_id or ""
            payment.raw_payload = event.to_dict_recursive()
            payment.save(
                update_fields=[
                    "status",
                    "stripe_payment_intent_id",
                    "raw_payload",
                    "updated_at",
                ]
            )

        confirm_booking_after_payment(booking.id)

    elif event_type == "checkout.session.expired":
        session = event_data
        booking_id = session.get("metadata", {}).get("booking_id")
        stripe_session_id = session.get("id")

        if booking_id:
            Payment.objects.filter(
                booking_id=booking_id,
                stripe_session_id=stripe_session_id,
            ).update(status="failed", raw_payload=event.to_dict_recursive())

            try:
                booking = Booking.objects.get(id=booking_id, status="pending")
                booking.status = "expired"
                booking.save(update_fields=["status"])
                booking.seats.update(status="available", held_until=None)

                schedule = booking.schedule
                schedule.available_seats = schedule.seats.filter(status="available").count()
                schedule.save(update_fields=["available_seats"])
            except Booking.DoesNotExist:
                pass

    elif event_type == "payment_intent.payment_failed":
        intent = event_data
        payment_intent_id = intent.get("id")

        payment = Payment.objects.filter(
            stripe_payment_intent_id=payment_intent_id
        ).select_related("booking").first()

        if payment:
            payment.status = "failed"
            payment.raw_payload = event.to_dict_recursive()
            payment.save(update_fields=["status", "raw_payload", "updated_at"])

            booking = payment.booking
            if booking.status == "pending":
                booking.status = "cancelled"
                booking.save(update_fields=["status"])
                booking.seats.update(status="available", held_until=None)

                schedule = booking.schedule
                schedule.available_seats = schedule.seats.filter(status="available").count()
                schedule.save(update_fields=["available_seats"])

    return event