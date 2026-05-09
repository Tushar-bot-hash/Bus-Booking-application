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
    "whitenoise.runserver_nostatic",  # Added for whitenoise
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
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = "bus_booking.urls"
WSGI_APPLICATION = "bus_booking.wsgi.application"

# Database
DATABASES = {"default": env.db()}

# Custom user model
AUTH_USER_MODEL = "users.User"

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # Changed to IST for India
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (User uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ============ CORS & CSRF SETTINGS ============
# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "https://bus-booking-application-gamma.vercel.app",
    "https://bus-booking-application-tusharv811-2882s-projects.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]

# Allow credentials (cookies, authorization headers)
CORS_ALLOW_CREDENTIALS = True

# Allow all necessary methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',  # Important for preflight requests
    'PATCH',
    'POST',
    'PUT',
]

# Allow all necessary headers
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

# Preflight cache duration
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
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
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
    "AUTH_COOKIE_SECURE": not DEBUG,
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_SAMESITE": "None" if not DEBUG else "Lax",
    "AUTH_COOKIE_PATH": "/",
    "AUTH_COOKIE_DOMAIN": None,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}

# ============ REST FRAMEWORK SETTINGS ============
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "users.authentication.CookieJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# ============ DRF SPECTACULAR (API Documentation) ============
SPECTACULAR_SETTINGS = {
    "TITLE": "Bus Ticket Booking API",
    "DESCRIPTION": "API for booking bus tickets in India",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# ============ STRIPE SETTINGS ============
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET")
FRONTEND_URL = env("FRONTEND_URL", default="http://localhost:5173")

# ============ EMAIL SETTINGS (Optional - Add if needed) ============
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
# EMAIL_PORT = env.int("EMAIL_PORT", default=587)
# EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
# EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

# ============ CELERY SETTINGS (Optional - Add if using Celery) ============
# CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379")
# CELERY_RESULT_BACKEND = env("REDIS_URL", default="redis://localhost:6379")
# CELERY_ACCEPT_CONTENT = ["application/json"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"

# ============ LOGGING SETTINGS ============
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Debug CORS on startup (remove after confirming it works)
if not DEBUG:
    print("=== Production CORS Settings ===")
    print(f"CORS_ALLOWED_ORIGINS: {CORS_ALLOWED_ORIGINS}")
    print(f"CORS_ALLOW_CREDENTIALS: {CORS_ALLOW_CREDENTIALS}")
    print(f"SESSION_COOKIE_SAMESITE: {SESSION_COOKIE_SAMESITE}")
    print(f"CSRF_COOKIE_SAMESITE: {CSRF_COOKIE_SAMESITE}")