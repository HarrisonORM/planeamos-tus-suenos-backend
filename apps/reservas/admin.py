from django.contrib import admin
from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = [
        "nombre_cliente",
        "tipo_reserva",
        "fecha_evento",
        "valor_total",
        "estado",
    ]
    list_filter = ["estado", "tipo_reserva"]
    search_fields = [
        "nombre_cliente",
        "correo",
    ]