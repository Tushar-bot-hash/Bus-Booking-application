from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, 
    CookieTokenObtainPairView, 
    MeView, 
    LogoutView
)

urlpatterns = [
    # Auth Endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CookieTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Profile & Token Endpoints
    path('me/', MeView.as_view(), name='user_profile'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]