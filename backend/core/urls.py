# backend/core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Public
    path("operators/", views.BusOperatorListView.as_view(), name="operator-list"),
    path("routes/", views.RouteListView.as_view(), name="route-list"),
    path("search/", views.BusSearchView.as_view(), name="bus-search"),
    path("schedules/<int:pk>/", views.ScheduleDetailView.as_view(), name="schedule-detail"),
    path("schedules/<int:pk>/seats/", views.SeatLayoutView.as_view(), name="seat-layout"),

    # Authenticated booking flow
    path("booking/create/", views.CreateBookingView.as_view(), name="create-booking"),
    path("booking/<uuid:pk>/", views.BookingDetailView.as_view(), name="booking-detail"),
    path("booking/<uuid:pk>/pay/", views.CreateStripeCheckoutView.as_view(), name="create-checkout"),

    # My tickets
    path("my-bookings/", views.MyBookingsView.as_view(), name="my-bookings"),
    path("my-bookings/<uuid:pk>/", views.MyBookingDetailView.as_view(), name="my-booking-detail"),
    path("my-bookings/<uuid:pk>/cancel/", views.CancelBookingView.as_view(), name="cancel-booking"),
    path("my-bookings/<uuid:pk>/ticket-pdf/", views.TicketPDFView.as_view(), name="ticket-pdf"),
]