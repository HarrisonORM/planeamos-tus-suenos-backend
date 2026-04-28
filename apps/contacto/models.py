from django.db import models


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.nombre} — {self.correo}"


class Cotizacion(models.Model):
    TIPOS_EVENTO = [
        ("boda", "Boda"),
        ("quinceañera", "Quinceañera"),
        ("fiesta", "Fiesta"),
        ("corporativo", "Corporativo"),
        ("otro", "Otro"),
    ]

    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    tipo_evento = models.CharField(
        max_length=50, choices=TIPOS_EVENTO
    )
    fecha_evento = models.DateField()
    num_invitados = models.IntegerField()
    municipio = models.CharField(max_length=100)
    tiene_locacion = models.BooleanField(
        default=False
    )
    servicios_interes = models.JSONField(
        default=list
    )
    mensaje = models.TextField(blank=True)
    atendido = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ["-creado"]

    def __str__(self):
        tipo = self.get_tipo_evento_display()
        return f"{self.nombre} — {tipo}"