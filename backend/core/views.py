from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from core.services.stripe_service import handle_stripe_webhook


from .models import Booking
from .services.stripe_service import create_stripe_checkout_session, handle_stripe_webhook

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        event = handle_stripe_webhook(payload, sig_header)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    return Response({"received": True})

class CreateStripeCheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            booking = (
                Booking.objects.select_related(
                    "user",
                    "schedule",
                    "schedule__bus",
                    "schedule__bus__route",
                )
                .prefetch_related("seats")
                .get(pk=pk, user=request.user)
            )
        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if booking.status != "pending":
            return Response(
                {"detail": "Only pending bookings can be paid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = create_stripe_checkout_session(booking)

        return Response(
            {
                "checkout_url": session.url,
                "session_id": session.id,
            },
            status=status.HTTP_200_OK,
        )