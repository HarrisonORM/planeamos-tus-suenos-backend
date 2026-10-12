from rest_framework import viewsets
from .models import (
    Locacion,
    Paquete,
    ProductoAlquiler,
    ServicioPersonal,
)
from .serializers import (
    LocacionSerializer,
    PaqueteSerializer,
    ProductoAlquilerSerializer,
    ServicioPersonalSerializer,
)


class ProductoAlquilerViewSet(viewsets.ModelViewSet):
    queryset = ProductoAlquiler.objects.filter(
        disponible=True
    )
    serializer_class = ProductoAlquilerSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.request.query_params.get(
            "categoria"
        )
        if categoria:
            qs = qs.filter(categoria=categoria)
        return qs


class ServicioPersonalViewSet(viewsets.ModelViewSet):
    queryset = ServicioPersonal.objects.filter(
        disponible=True
    )
    serializer_class = ServicioPersonalSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.request.query_params.get(
            "categoria"
        )
        if categoria:
            qs = qs.filter(categoria=categoria)
        return qs


class PaqueteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Paquete.objects.all()
    serializer_class = PaqueteSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        tipo_evento = self.request.query_params.get(
            "tipo_evento"
        )
        if tipo_evento:
            qs = qs.filter(tipo_evento=tipo_evento)
        return qs


class LocacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Locacion.objects.all()
    serializer_class = LocacionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        municipio = self.request.query_params.get(
            "municipio"
        )
        if municipio:
            qs = qs.filter(municipio__iexact=municipio)
        return qs