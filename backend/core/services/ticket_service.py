# backend/core/services/ticket_service.py
import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from core.models import Booking, Seat, Schedule, Payment
from decimal import Decimal

def generate_pnr():
    """Generate unique 10-digit PNR like Indian Railways / RedBus"""
    return "BUS" + str(uuid.uuid4().int)[:7]

def hold_seats(schedule: Schedule, seat_numbers: list, minutes: int = 10):
    """Hold seats temporarily for payment window"""
    held_until = timezone.now() + timedelta(minutes=minutes)
    
    seats = Seat.objects.filter(
        schedule=schedule,
        seat_number__in=seat_numbers,
        status="available"
    )
    
    if seats.count() != len(seat_numbers):
        return False, "Some seats are no longer available"
    
    seats.update(status="held", held_until=held_until)
    return True, seats

def release_expired_holds():
    """Release seats held for more than 10 minutes (run via Celery beat or management command)"""
    expired = Seat.objects.filter(
        status="held",
        held_until__lt=timezone.now()
    )
    count = expired.update(status="available", held_until=None)
    return count

@transaction.atomic
def create_booking(user, schedule, seats, passenger_details):
    """Main booking creation with GST calculation (India)"""
    # Calculate total + GST (5% for bus tickets in India)
    base_amount = sum(seat.price for seat in seats)
    gst_rate = Decimal("0.05")  # 5% GST on bus tickets
    gst_amount = base_amount * gst_rate
    total_amount = base_amount + gst_amount

    booking = Booking.objects.create(
        user=user,
        schedule=schedule,
        passenger_name=passenger_details["name"],
        passenger_phone=passenger_details["phone"],
        passenger_email=passenger_details["email"],
        total_amount=total_amount,
        gst_amount=gst_amount,
        status="pending",
        expires_at=timezone.now() + timedelta(minutes=15),
        pnr_number=generate_pnr(),
    )
    
    booking.seats.set(seats)
    
    # Update seat status
    seats.update(status="held", held_until=booking.expires_at)
    
    # Update available seats count
    schedule.available_seats = schedule.seats.filter(status="available").count()
    schedule.save(update_fields=["available_seats"])
    
    return booking

@transaction.atomic
def confirm_booking_after_payment(booking_id):
    """Call this when Stripe webhook confirms payment"""
    try:
        booking = Booking.objects.select_related("schedule").get(id=booking_id, status="pending")
    except Booking.DoesNotExist:
        return False, "Booking not found or already processed"
    
    booking.status = "confirmed"
    booking.save(update_fields=["status"])
    
    # Permanently book seats
    booking.seats.update(status="booked", held_until=None)
    
    # Update schedule
    booking.schedule.available_seats = booking.schedule.seats.filter(status="available").count()
    booking.schedule.save(update_fields=["available_seats"])
    
    return True, booking

@transaction.atomic
def cancel_booking(booking_id):
    """Cancel booking and release seats"""
    try:
        booking = Booking.objects.get(id=booking_id, status__in=["pending", "confirmed"])
    except Booking.DoesNotExist:
        return False, "Booking not found"
    
    booking.status = "cancelled"
    booking.save(update_fields=["status"])
    
    # Release seats
    booking.seats.update(status="available", held_until=None)
    
    # Update schedule
    booking.schedule.available_seats = booking.schedule.seats.filter(status="available").count()
    booking.schedule.save(update_fields=["available_seats"])
    
    return True, booking