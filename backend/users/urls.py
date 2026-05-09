from django.urls import path
from .views import RegisterView, CookieTokenObtainPairView, MeView, LogoutView, CookieTokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CookieTokenObtainPairView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]