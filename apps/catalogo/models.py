from django.db import models


class ProductoAlquiler(models.Model):
    CATEGORIAS = [
        ("mobiliario", "Mobiliario"),
        ("menaje", "Menaje y Cristalería"),
        ("sonido", "Sonido"),
        ("iluminacion", "Iluminación"),
        ("decoracion", "Decoración"),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(
        max_length=50, choices=CATEGORIAS
    )
    precio = models.IntegerField()
    unidad = models.CharField(
        max_length=50, default="por día"
    )
    imagen = models.URLField(blank=True)
    disponible = models.BooleanField(default=True)
    tipos_evento = models.JSONField(default=list)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto de Alquiler"
        verbose_name_plural = "Productos de Alquiler"
        ordering = ["categoria", "nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"


class ServicioPersonal(models.Model):
    CATEGORIAS = [
        ("meseros", "Meseros"),
        ("chef", "Chef"),
        ("dj", "DJ"),
        ("reposteria", "Repostería"),
        ("fotografia", "Fotografía"),
        ("floreria", "Florería"),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(
        max_length=50, choices=CATEGORIAS
    )
    precio = models.IntegerField()
    unidad = models.CharField(
        max_length=50, default="por evento"
    )
    imagen = models.URLField(blank=True)
    disponible = models.BooleanField(default=True)
    tipos_evento = models.JSONField(default=list)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Servicio de Personal"
        verbose_name_plural = "Servicios de Personal"
        ordering = ["categoria", "nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"


class Paquete(models.Model):
    TIPOS_EVENTO = [
        ("boda", "Boda"),
        ("quinceañera", "Quinceañera"),
        ("fiesta", "Fiesta"),
        ("corporativo", "Corporativo"),
        ("otro", "Otro"),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_evento = models.CharField(
        max_length=50,
        choices=TIPOS_EVENTO,
    )
    precio_desde = models.PositiveIntegerField()
    precio_hasta = models.PositiveIntegerField()
    incluye = models.JSONField(default=list)
    imagen = models.URLField(blank=True)
    destacado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"
        ordering = ["-destacado", "nombre"]

    def __str__(self):
        return self.nombre


class Locacion(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    municipio = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    precio = models.CharField(
        max_length=50,
        default="Consultar",
    )
    imagen = models.URLField(blank=True)
    tipos_evento = models.JSONField(default=list)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Locación"
        verbose_name_plural = "Locaciones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre