from django.contrib import admin
from .models import EventoPortafolio


@admin.register(EventoPortafolio)
class EventoPortafolioAdmin(admin.ModelAdmin):
    list_display = [
        "titulo",
        "tipo_evento",
        "lugar",
        "fecha",
    ]
    list_filter = ["tipo_evento"]
    search_fields = ["titulo", "lugar"]