from django.db import models


class EventoPortafolio(models.Model):
    TIPOS_EVENTO = [
        ("boda", "Boda"),
        ("quinceañera", "Quinceañera"),
        ("fiesta", "Fiesta"),
        ("corporativo", "Corporativo"),
        ("otro", "Otro"),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo_evento = models.CharField(
        max_length=50, choices=TIPOS_EVENTO
    )
    imagen = models.URLField()
    fecha = models.DateField()
    lugar = models.CharField(max_length=200)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Evento del Portafolio"
        verbose_name_plural = "Eventos del Portafolio"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.titulo} — {self.lugar}"