from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import User
from .models import BusOperator, Route, Bus, Schedule, Seat, Booking, Payment

# User Serializers (for users app, but needed here)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'phone')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    phone_number = serializers.CharField(source='phone', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name', 
                  'phone_number', 'date_of_birth', 'profile_picture', 
                  'is_verified', 'date_joined')
        read_only_fields = ('id', 'email', 'is_verified', 'date_joined')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

# Core Model Serializers
class BusOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusOperator
        fields = ['id', 'name', 'code', 'contact_email', 'contact_phone', 'is_active']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'origin', 'destination', 'distance_km', 'duration_minutes', 'is_active']

class BusSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.name', read_only=True)
    route_name = serializers.CharField(source='route.origin', read_only=True)
    
    class Meta:
        model = Bus
        fields = ['id', 'bus_number', 'name', 'operator_name', 'route_name', 'total_seats', 'layout', 'is_active']

class ScheduleSerializer(serializers.ModelSerializer):
    bus = BusSerializer(read_only=True)
    origin = serializers.CharField(source='bus.route.origin', read_only=True)
    destination = serializers.CharField(source='bus.route.destination', read_only=True)
    operator_name = serializers.CharField(source='bus.operator.name', read_only=True)
    
    class Meta:
        model = Schedule
        fields = ['id', 'bus', 'departure_time', 'arrival_time', 'base_fare', 
                  'available_seats', 'is_active', 'origin', 'destination', 'operator_name']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'status', 'price', 'held_until']

class BookingSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)
    schedule_details = ScheduleSerializer(source='schedule', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'reference_code', 'schedule', 'schedule_details', 'seats', 
                  'passenger_name', 'passenger_phone', 'passenger_email', 
                  'total_amount', 'gst_amount', 'status', 'created_at', 'expires_at']

class MyBookingSerializer(serializers.ModelSerializer):
    schedule_details = ScheduleSerializer(source='schedule', read_only=True)
    seat_numbers = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = ['id', 'reference_code', 'schedule_details', 'seat_numbers', 
                  'passenger_name', 'passenger_phone', 'total_amount', 'status', 'created_at']
    
    def get_seat_numbers(self, obj):
        return [seat.seat_number for seat in obj.seats.all()]
