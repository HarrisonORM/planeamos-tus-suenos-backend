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
    valor_total = models.IntegerField(default=0)
    valor_anticipo = models.IntegerField(default=0)
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