from rest_framework import serializers
from .models import (
    Locacion,
    Paquete,
    ProductoAlquiler,
    ServicioPersonal,
)


class ProductoAlquilerSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = ProductoAlquiler
        fields = "__all__"


class ServicioPersonalSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = ServicioPersonal
        fields = "__all__"


class PaqueteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paquete
        fields = "__all__"


class LocacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locacion
        fields = "__all__"