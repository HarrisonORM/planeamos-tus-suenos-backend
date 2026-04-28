from rest_framework import serializers
from .models import ProductoAlquiler, ServicioPersonal


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