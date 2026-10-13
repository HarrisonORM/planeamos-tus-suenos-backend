import uuid
from django.db import models


class Reserva(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("anticipo_pagado", "Anticipo Pagado"),
        ("confirmada", "Confirmada"),
        ("completada", "Completada"),
        ("cancelada", "Cancelada"),
    ]

    TIPOS_RESERVA = [
        ("alquiler", "Alquiler"),
        ("servicio", "Servicio"),
        ("evento", "Evento Completo"),
    ]

    nombre_cliente = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    direccion = models.TextField(blank=True)
    tipo_reserva = models.CharField(
        max_length=50, choices=TIPOS_RESERVA
    )
    fecha_evento = models.DateField()
    descripcion = models.TextField(blank=True)
    detalle = models.JSONField(default=list, blank=True)
    valor_total = models.IntegerField(default=0)
    valor_anticipo = models.IntegerField(default=0)
    anticipo_validado = models.BooleanField(default=False)
    token_pago = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        null=True,
        blank=True,
    )
    estado = models.CharField(
        max_length=50,
        choices=ESTADOS,
        default="pendiente",
    )
    notas = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-creado"]

    def __str__(self):
        return (
            f"{self.nombre_cliente} — "
            + f"{self.get_estado_display()}"
        )


class PagoReserva(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
        ("anulado", "Anulado"),
        ("error", "Error"),
    ]

    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.PROTECT,
        related_name="pagos",
    )
    referencia = models.CharField(
        max_length=255,
        unique=True,
    )
    valor_anticipo = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente",
    )
    transaccion_id = models.CharField(
        max_length=100,
        blank=True,
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pago de Reserva"
        verbose_name_plural = "Pagos de Reservas"
        ordering = ["-creado"]

    def __str__(self):
        return (
            f"{self.referencia} — "
            + f"{self.get_estado_display()}"
        )