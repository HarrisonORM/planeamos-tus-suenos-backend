from rest_framework import serializers
from .models import Reserva


class ReservaSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Reserva
        fields = "__all__"


class SolicitudReservaSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Reserva
        fields = [
            "id",
            "nombre_cliente",
            "telefono",
            "correo",
            "direccion",
            "tipo_reserva",
            "fecha_evento",
            "descripcion",
            "valor_total",
            "valor_anticipo",
            "token_pago",
            "estado",
            "notas",
            "creado",
            "actualizado",
        ]
        read_only_fields = [
            "id",
            "token_pago",
            "estado",
            "notas",
            "creado",
            "actualizado",
        ]