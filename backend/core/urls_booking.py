from django.urls import path
from .views import CreateBookingView, BookingDetailView, CreateStripeCheckoutView

urlpatterns = [
    path("create/", CreateBookingView.as_view(), name="create-booking"),
    path("<uuid:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("<uuid:pk>/pay/", CreateStripeCheckoutView.as_view(), name="create-checkout"),
]