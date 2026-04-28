from django.contrib import admin
from .models import ProductoAlquiler, ServicioPersonal


@admin.register(ProductoAlquiler)
class ProductoAlquilerAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "categoria",
        "precio",
        "disponible",
    ]
    list_filter = ["categoria", "disponible"]
    search_fields = ["nombre", "descripcion"]


@admin.register(ServicioPersonal)
class ServicioPersonalAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "categoria",
        "precio",
        "disponible",
    ]
    list_filter = ["categoria", "disponible"]
    search_fields = ["nombre", "descripcion"]