from django.urls import path
from .views import BusOperatorListView

urlpatterns = [
    path("", BusOperatorListView.as_view(), name="operator-list"),
]
