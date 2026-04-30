from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Django Rest Framework Imports
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Local Imports
from .models import Booking
from .services.stripe_service import create_stripe_checkout_session, handle_stripe_webhook

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        # Use the local service import
        event = handle_stripe_webhook(payload, sig_header)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"received": True}, status=status.HTTP_200_OK)

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

        try:
            session = create_stripe_checkout_session(booking)
            return Response(
                {
                    "checkout_url": session.url,
                    "session_id": session.id,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": f"Stripe session creation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )