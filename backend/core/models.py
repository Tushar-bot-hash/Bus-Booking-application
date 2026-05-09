from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class BusOperator(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, unique=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    origin = models.CharField(max_length=120)
    destination = models.CharField(max_length=120)
    distance_km = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("origin", "destination")

    def __str__(self):
        return f"{self.origin} → {self.destination}"


class Bus(models.Model):
    operator = models.ForeignKey(BusOperator, on_delete=models.CASCADE, related_name="buses")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="buses")
    name = models.CharField(max_length=120)
    bus_number = models.CharField(max_length=30, unique=True)
    total_seats = models.PositiveSmallIntegerField(default=40)
    layout = models.JSONField(default=dict, help_text="Seat layout metadata")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bus_number} ({self.name})"


class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="schedules")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["departure_time"]

    def save(self, *args, **kwargs):
        # Only auto-initialize available_seats on first creation (INSERT),
        # not on every subsequent UPDATE (which would overwrite service logic).
        if self._state.adding and self.available_seats == 0 and self.bus_id:
            self.available_seats = self.bus.total_seats
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bus.bus_number} | {self.departure_time:%d-%m %H:%M} → {self.arrival_time:%H:%M}"


class Seat(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=[
        ("available", "Available"),
        ("booked", "Booked"),
        ("held", "Held"),
        ("blocked", "Blocked"),
    ], default="available")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    held_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("schedule", "seat_number")

    def __str__(self):
        return f"{self.schedule_id} - {self.seat_number} ({self.status})"


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="bookings")
    seats = models.ManyToManyField(Seat, related_name="bookings")
    passenger_name = models.CharField(max_length=120)
    passenger_phone = models.CharField(max_length=20)
    passenger_email = models.EmailField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ADDED
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
        ("refunded", "Refunded"),
    ], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    reference_code = models.CharField(max_length=40, unique=True, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True)

    @property
    def pnr_number(self):
        """Alias for reference_code to maintain compatibility with service code"""
        return self.reference_code

    def __str__(self):
        return f"{self.reference_code} - {self.user.email} - ₹{self.total_amount}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    provider = models.CharField(max_length=20, default="stripe")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="inr")
    status = models.CharField(max_length=20, choices=[
        ("initiated", "Initiated"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ], default="initiated")
    stripe_session_id = models.CharField(max_length=200, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True)
    raw_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking.reference_code} - {self.status} - ₹{self.amount}"