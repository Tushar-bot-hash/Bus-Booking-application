from django.urls import path
from .views import MyBookingsView, MyBookingDetailView, CancelBookingView, TicketPDFView

urlpatterns = [
    path("", MyBookingsView.as_view(), name="my-bookings"),
    path("<uuid:pk>/", MyBookingDetailView.as_view(), name="my-booking-detail"),
    path("<uuid:pk>/cancel/", CancelBookingView.as_view(), name="cancel-booking"),
    path("<uuid:pk>/ticket-pdf/", TicketPDFView.as_view(), name="ticket-pdf"),
]