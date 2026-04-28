from rest_framework import viewsets, mixins
from .models import MensajeContacto, Cotizacion
from .serializers import (
    MensajeContactoSerializer,
    CotizacionSerializer,
)


class MensajeContactoViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = MensajeContacto.objects.all()
    serializer_class = MensajeContactoSerializer


class CotizacionViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Cotizacion.objects.all()
    serializer_class = CotizacionSerializer