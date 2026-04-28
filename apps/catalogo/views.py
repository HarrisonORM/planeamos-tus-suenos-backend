from rest_framework import viewsets
from .models import ProductoAlquiler, ServicioPersonal
from .serializers import (
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