from django.contrib import admin
from django.utils.html import format_html
from .models import BusOperator, Route, Bus, Schedule, Seat, Booking, Payment

@admin.register(BusOperator)
class BusOperatorAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    search_fields = ("name", "code")
    list_filter = ("is_active",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("origin", "destination", "distance_km", "duration_minutes", "is_active")
    search_fields = ("origin", "destination")
    list_filter = ("is_active",)


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("bus_number", "name", "operator", "route", "total_seats", "is_active")
    search_fields = ("bus_number", "name")
    list_filter = ("operator", "route", "is_active")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("bus", "departure_time", "arrival_time", "base_fare", "available_seats", "is_active")
    list_filter = ("bus__route", "bus__operator", "departure_time", "is_active")
    search_fields = ("bus__bus_number", "bus__name")
    date_hierarchy = "departure_time"


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("schedule", "seat_number", "status", "price", "held_until")
    list_filter = ("status", "schedule__bus__route")
    search_fields = ("seat_number", "schedule__bus__bus_number")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("reference_code", "user", "schedule", "total_amount", "status", "created_at")
    list_filter = ("status", "schedule__bus__route", "created_at")
    search_fields = ("reference_code", "user__email", "passenger_name", "passenger_phone")
    readonly_fields = ("id", "created_at", "updated_at")
    actions = ["mark_confirmed", "mark_cancelled"]

    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status="confirmed")
        self.message_user(request, f"{updated} bookings marked confirmed.")

    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status="cancelled")
        self.message_user(request, f"{updated} bookings marked cancelled.")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("booking", "provider", "amount", "currency", "status", "created_at")
    list_filter = ("status", "provider", "created_at")
    search_fields = ("booking__reference_code", "stripe_session_id", "stripe_payment_intent_id")
    readonly_fields = ("created_at", "updated_at", "raw_payload")