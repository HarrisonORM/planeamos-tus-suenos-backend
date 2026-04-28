from rest_framework import serializers
from .models import EventoPortafolio


class EventoPortafolioSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = EventoPortafolio
        fields = "__all__"