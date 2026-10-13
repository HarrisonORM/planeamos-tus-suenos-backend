from django.utils import timezone
from rest_framework import serializers
from apps.catalogo.models import (
    ProductoAlquiler,
    ServicioPersonal,
)
from .models import Reserva


class ItemSolicitudReservaSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    tipo = serializers.ChoiceField(
        choices=["producto", "servicio"]
    )
    cantidad = serializers.IntegerField(
        min_value=1,
        max_value=1000,
    )


class ReservaSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Reserva
        fields = "__all__"


class SolicitudReservaSerializer(
    serializers.ModelSerializer
):
    items = ItemSolicitudReservaSerializer(
        many=True,
        write_only=True,
        allow_empty=False,
    )

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
            "items",
            "detalle",
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
            "tipo_reserva",
            "detalle",
            "valor_total",
            "valor_anticipo",
            "token_pago",
            "estado",
            "notas",
            "creado",
            "actualizado",
        ]

    def validate(self, attrs):
        fecha_evento = attrs["fecha_evento"]
        if fecha_evento < timezone.localdate():
            raise serializers.ValidationError({
                "fecha_evento":
                    "La fecha del evento no puede estar en el pasado."
            })

        fecha_ocupada = Reserva.objects.filter(
            fecha_evento=fecha_evento,
            estado__in=["anticipo_pagado", "confirmada"],
        ).exists()
        if fecha_ocupada:
            raise serializers.ValidationError({
                "fecha_evento":
                    "Esta fecha ya está ocupada. Elige otra."
            })

        items = attrs["items"]
        llaves = [
            (item["tipo"], item["id"])
            for item in items
        ]
        if len(llaves) != len(set(llaves)):
            raise serializers.ValidationError({
                "items":
                    "No repitas el mismo producto o servicio."
            })

        detalle = []
        total = 0
        tipos = set()
        for item in items:
            tipo = item["tipo"]
            modelo = (
                ProductoAlquiler
                if tipo == "producto"
                else ServicioPersonal
            )
            articulo = modelo.objects.filter(
                pk=item["id"],
                disponible=True,
            ).first()
            if articulo is None:
                raise serializers.ValidationError({
                    "items":
                        (
                            "Uno de los productos o servicios "
                            "ya no está disponible."
                        )
                })

            subtotal = articulo.precio * item["cantidad"]
            total += subtotal
            tipos.add(tipo)
            detalle.append({
                "id": articulo.pk,
                "tipo": tipo,
                "nombre": articulo.nombre,
                "cantidad": item["cantidad"],
                "precio_unitario": articulo.precio,
                "unidad": articulo.unidad,
                "subtotal": subtotal,
            })

        attrs["detalle"] = detalle
        attrs["valor_total"] = total
        attrs["valor_anticipo"] = 0
        attrs["tipo_reserva"] = (
            "alquiler"
            if tipos == {"producto"}
            else "servicio"
            if tipos == {"servicio"}
            else "evento"
        )
        attrs.pop("items")
        return attrs
