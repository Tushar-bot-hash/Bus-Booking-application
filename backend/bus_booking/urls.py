from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# CORS Debug View - Add this temporarily to test CORS
@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def cors_debug(request):
    """Test endpoint to verify CORS is working"""
    response = JsonResponse({
        "status": "success",
        "message": "CORS is configured correctly!",
        "method": request.method,
        "headers": {
            "origin": request.headers.get("origin", "No origin header"),
            "content_type": request.headers.get("content-type", "Not set"),
        }
    })
    
    # Manually set CORS headers as a fallback
    origin = request.headers.get("origin")
    if origin:
        response["Access-Control-Allow-Origin"] = origin
        response["Access-Control-Allow-Credentials"] = "true"
    
    if request.method == "OPTIONS":
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-CSRFToken"
        
    return response

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        "status": "healthy",
        "message": "API is running"
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # CORS Test Endpoints (remove after testing)
    path("api/cors-debug/", cors_debug, name="cors-debug"),
    path("api/health/", health_check, name="health-check"),

    # API Routes
    path("api/auth/", include("users.urls")),
    path("api/", include("core.urls")),

    # Stripe Webhook (must be raw body + no CSRF)
    path("api/webhook/stripe/", include("core.urls_webhook")),

    # API Documentation (beautiful Swagger + Redoc)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]