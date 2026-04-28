from django.contrib import admin
from .models import MensajeContacto, Cotizacion


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "correo",
        "leido",
        "creado",
    ]
    list_filter = ["leido"]
    search_fields = ["nombre", "correo", "mensaje"]


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "tipo_evento",
        "fecha_evento",
        "num_invitados",
        "atendido",
    ]
    list_filter = ["tipo_evento", "atendido"]
    search_fields = ["nombre", "correo"]