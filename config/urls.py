from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def bienvenida(request):
    return JsonResponse({
        "empresa": "Planeamos tus Sueños",
        "estado": "API funcionando",
        "endpoints": {
            "catalogo": "/api/catalogo/",
            "portafolio": "/api/portafolio/",
            "contacto": "/api/contacto/",
            "reservas": "/api/reservas/",
            "admin": "/admin/",
        },
    })


urlpatterns = [
    path("", bienvenida),
    path("admin/", admin.site.urls),
    path(
        "api/catalogo/",
        include("apps.catalogo.urls"),
    ),
    path(
        "api/portafolio/",
        include("apps.portafolio.urls"),
    ),
    path(
        "api/contacto/",
        include("apps.contacto.urls"),
    ),
    path(
        "api/reservas/",
        include("apps.reservas.urls"),
    ),
]

admin.site.site_header = (
    "Planeamos tus Sueños — Panel Administrativo"
)
admin.site.site_title = "Planeamos tus Sueños"
admin.site.index_title = "Panel de Control"