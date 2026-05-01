import os
import environ
from datetime import timedelta
from pathlib import Path

env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env("SECRET_KEY")

# --- ALLOWED HOSTS (Local + Production) ---
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[
    "bus-booking-application-4.onrender.com",
    "localhost",
    "127.0.0.1",
    "0.0.0.0"
])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "users",
    "core",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Must be FIRST
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bus_booking.urls"
WSGI_APPLICATION = "bus_booking.wsgi.application"

DATABASES = {"default": env.db()}
AUTH_USER_MODEL = "users.User"

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ============ UPDATED CORS & CSRF SETTINGS ============
# CORS Settings - Fixed for credentials
CORS_ALLOWED_ORIGINS = [
    "https://bus-booking-application-gamma.vercel.app",
    "https://bus-booking-application-tusharv811-2882s-projects.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]

# Critical for withCredentials
CORS_ALLOW_CREDENTIALS = True

# Explicitly allow all necessary methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',  # Important for preflight requests
    'PATCH',
    'POST',
    'PUT',
]

# Explicitly allow all necessary headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Expose headers to frontend
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    "https://bus-booking-application-gamma.vercel.app",
    "https://bus-booking-application-tusharv811-2882s-projects.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]

# Make sure preflight requests aren't cached too long (optional)
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours

# ============ SECURITY SETTINGS ============
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if DEBUG:
    # Local Development Settings
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"
else:
    # Production Settings (Render/Vercel)
    # Must be True for HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # 'None' required for cross-site requests with credentials
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"

# ============ JWT SETTINGS ============
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_COOKIE": "access_token",
    "AUTH_COOKIE_REFRESH": "refresh_token",
    "AUTH_COOKIE_SECURE": not DEBUG,  # True in production
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_SAMESITE": "None" if not DEBUG else "Lax",  # 'None' for cross-site
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# ============ OTHER SETTINGS ============
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET")
FRONTEND_URL = env("FRONTEND_URL")

# Debug CORS on startup (remove after confirming it works)
if not DEBUG:
    print("=== Production CORS Settings ===")
    print(f"CORS_ALLOWED_ORIGINS: {CORS_ALLOWED_ORIGINS}")
    print(f"CORS_ALLOW_CREDENTIALS: {CORS_ALLOW_CREDENTIALS}")
    print(f"SESSION_COOKIE_SAMESITE: {SESSION_COOKIE_SAMESITE}")
    print(f"CSRF_COOKIE_SAMESITE: {CSRF_COOKIE_SAMESITE}")