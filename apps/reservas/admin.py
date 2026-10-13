from django.contrib import admin
from .models import PagoReserva, Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = [
        "nombre_cliente",
        "tipo_reserva",
        "fecha_evento",
        "valor_total",
        "valor_anticipo",
        "anticipo_validado",
        "estado",
    ]
    list_filter = ["estado", "tipo_reserva"]
    search_fields = [
        "nombre_cliente",
        "correo",
    ]
    readonly_fields = ["detalle"]


@admin.register(PagoReserva)
class PagoReservaAdmin(admin.ModelAdmin):
    list_display = [
        "referencia",
        "reserva",
        "valor_anticipo",
        "estado",
        "transaccion_id",
        "creado",
    ]
    list_filter = ["estado"]
    search_fields = [
        "referencia",
        "transaccion_id",
        "reserva__nombre_cliente",
    ]
    readonly_fields = [
        "reserva",
        "referencia",
        "valor_anticipo",
        "estado",
        "transaccion_id",
        "creado",
        "actualizado",
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False