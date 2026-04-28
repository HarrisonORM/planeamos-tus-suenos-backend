from rest_framework import serializers
from .models import MensajeContacto, Cotizacion


class MensajeContactoSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = MensajeContacto
        fields = "__all__"


class CotizacionSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Cotizacion
        fields = "__all__"