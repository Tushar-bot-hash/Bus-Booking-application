from django.urls import path
from .views import BusSearchView, ScheduleDetailView, SeatLayoutView

urlpatterns = [
    path("", BusSearchView.as_view(), name="bus-search"),
    path("schedules/<int:pk>/", ScheduleDetailView.as_view(), name="schedule-detail"),
    path("schedules/<int:pk>/seats/", SeatLayoutView.as_view(), name="seat-layout"),
]