from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import io

# Django Rest Framework Imports
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Local Imports
from .models import BusOperator, Route, Schedule, Seat, Booking
from .serializers import (
    BusOperatorSerializer, RouteSerializer, ScheduleSerializer, 
    SeatSerializer, BookingSerializer, MyBookingSerializer
)
from .permissions import IsOwnerOrAdmin, IsBookingPending
from .services.payment_service import create_stripe_checkout_session, handle_stripe_webhook
from .services.ticket_service import create_booking, confirm_booking_after_payment, cancel_booking

# ============ STRIPE WEBHOOK ============
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        handle_stripe_webhook(payload, sig_header)
        return Response({"received": True}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ============ PUBLIC VIEWS ============
class BusOperatorListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        operators = BusOperator.objects.filter(is_active=True)
        serializer = BusOperatorSerializer(operators, many=True)
        return Response(serializer.data)

class RouteListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        routes = Route.objects.filter(is_active=True)
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

class BusSearchView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        origin = request.query_params.get('origin')
        destination = request.query_params.get('destination')
        date = request.query_params.get('date')
        
        if not all([origin, destination, date]):
            return Response(
                {"error": "origin, destination, and date are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filter schedules
        schedules = Schedule.objects.filter(
            bus__route__origin__icontains=origin,
            bus__route__destination__icontains=destination,
            departure_time__date=date,
            is_active=True,
            available_seats__gt=0
        ).select_related('bus', 'bus__route', 'bus__operator')
        
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

class ScheduleDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        schedule = get_object_or_404(Schedule, pk=pk, is_active=True)
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)

class SeatLayoutView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        schedule = get_object_or_404(Schedule, pk=pk)
        seats = schedule.seats.all()
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)

# ============ BOOKING VIEWS ============
class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        schedule_id = request.data.get('schedule_id')
        seat_numbers = request.data.get('seat_numbers', [])
        passenger_details = request.data.get('passenger_details', {})
        
        if not all([schedule_id, seat_numbers, passenger_details]):
            return Response(
                {"error": "schedule_id, seat_numbers, and passenger_details are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        schedule = get_object_or_404(Schedule, id=schedule_id, is_active=True)
        
        # Validate seats
        seats = Seat.objects.filter(
            schedule=schedule,
            seat_number__in=seat_numbers,
            status="available"
        )
        
        if seats.count() != len(seat_numbers):
            return Response(
                {"error": "Some seats are no longer available"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            booking = create_booking(
                user=request.user,
                schedule=schedule,
                seats=seats,
                passenger_details=passenger_details
            )
            
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        self.check_object_permissions(request, booking)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

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

# ============ MY BOOKINGS VIEWS ============
class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
        serializer = MyBookingSerializer(bookings, many=True)
        return Response(serializer.data)

class MyBookingDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        self.check_object_permissions(request, booking)
        serializer = MyBookingSerializer(booking)
        return Response(serializer.data)

class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin, IsBookingPending]
    
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        self.check_object_permissions(request, booking)
        
        if booking.status != "pending":
            return Response(
                {"error": "Only pending bookings can be cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success, result = cancel_booking(booking.id)
        if not success:
            return Response({"error": result}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)

class TicketPDFView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, user=request.user)
        self.check_object_permissions(request, booking)
        
        if booking.status != "confirmed":
            return Response(
                {"error": "Ticket PDF only available for confirmed bookings"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        
        # Add ticket content
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "BUS TICKET")
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 750, f"PNR: {booking.reference_code}")
        p.drawString(100, 730, f"Passenger: {booking.passenger_name}")
        p.drawString(100, 710, f"Phone: {booking.passenger_phone}")
        p.drawString(100, 690, f"From: {booking.schedule.bus.route.origin}")
        p.drawString(100, 670, f"To: {booking.schedule.bus.route.destination}")
        p.drawString(100, 650, f"Date: {booking.schedule.departure_time:%Y-%m-%d}")
        p.drawString(100, 630, f"Time: {booking.schedule.departure_time:%H:%M}")
        p.drawString(100, 610, f"Seats: {', '.join([s.seat_number for s in booking.seats.all()])}")
        p.drawString(100, 590, f"Amount: ₹{booking.total_amount}")
        
        p.save()
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{booking.reference_code}.pdf"'
        
        return response