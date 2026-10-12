from django.contrib import admin
from .models import (
    Locacion,
    Paquete,
    ProductoAlquiler,
    ServicioPersonal,
)


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


@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "tipo_evento",
        "precio_desde",
        "precio_hasta",
        "destacado",
    ]
    list_filter = ["tipo_evento", "destacado"]
    search_fields = ["nombre", "descripcion"]


@admin.register(Locacion)
class LocacionAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "municipio",
        "capacidad",
        "precio",
    ]
    list_filter = ["municipio"]
    search_fields = ["nombre", "municipio", "descripcion"]