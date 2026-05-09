from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

def set_auth_cookies(response, access_token, refresh_token):
    """
    Utility to set JWT tokens in HttpOnly cookies based on settings.py logic.
    """
    response.set_cookie(
        key=settings.SIMPLE_JWT["AUTH_COOKIE"],
        value=access_token,
        max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
    )
    response.set_cookie(
        key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
        value=refresh_token,
        max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
    )
    return response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens immediately upon registration
        refresh = RefreshToken.for_user(user)
        response = Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        
        return set_auth_cookies(response, str(refresh.access_token), str(refresh))


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom Login View that moves tokens from the JSON body into HttpOnly Cookies.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access = response.data.get("access")
            refresh = response.data.get("refresh")
            
            # Fetch user by email since request.user isn't available in Login POST
            email = request.data.get("email")
            try:
                user = User.objects.get(email=email)
                user.last_login_ip = request.META.get("REMOTE_ADDR")
                user.failed_login_attempts = 0
                user.save(update_fields=["last_login_ip", "failed_login_attempts"])
                
                # Replace standard response with user data + cookies
                res = Response({"user": UserSerializer(user).data})
                return set_auth_cookies(res, access, refresh)
            except User.DoesNotExist:
                return response # Fallback to standard error
                
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
        # Clear cookies by setting expiry to 0
        response.delete_cookie(
            settings.SIMPLE_JWT["AUTH_COOKIE"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
        )
        response.delete_cookie(
            settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
        )
        return response


class MeView(APIView):
    """
    Returns the current user profile. Used by the frontend on refresh 
    to check if the session is still active.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CookieTokenRefreshView(APIView):
    """
    Reads the refresh token from the HttpOnly cookie and issues a new
    access token (also written back as a cookie).
    The standard TokenRefreshView expects the token in the request body,
    which is inaccessible to JS — this fixes that.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_cookie_name = settings.SIMPLE_JWT.get("AUTH_COOKIE_REFRESH", "refresh_token")
        raw_token = request.COOKIES.get(refresh_cookie_name)

        if not raw_token:
            return Response(
                {"detail": "Refresh token cookie not found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(raw_token)
            access_token = str(refresh.access_token)

            # If ROTATE_REFRESH_TOKENS is True a new refresh token is also issued
            new_refresh = str(refresh) if settings.SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS") else raw_token
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response({"detail": "Token refreshed"}, status=status.HTTP_200_OK)
        return set_auth_cookies(response, access_token, new_refresh)