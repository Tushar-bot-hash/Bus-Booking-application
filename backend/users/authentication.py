from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that reads the access token from an HttpOnly
    cookie (set at login) instead of the Authorization header.

    Falls back to the standard Authorization header so that DRF Browsable API
    and tools like Postman / Swagger still work.
    """

    def authenticate(self, request):
        # 1. Try the cookie first
        cookie_name = settings.SIMPLE_JWT.get("AUTH_COOKIE", "access_token")
        raw_token = request.COOKIES.get(cookie_name)

        # 2. Fall back to the Authorization header
        if raw_token is None:
            header = self.get_header(request)
            if header is None:
                return None
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        try:
            user = self.get_user(validated_token)
        except AuthenticationFailed:
            raise

        return user, validated_token
