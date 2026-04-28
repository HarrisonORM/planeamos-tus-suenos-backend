from rest_framework import viewsets
from .models import Reserva
from .serializers import ReservaSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        estado = self.request.query_params.get(
            "estado"
        )
        if estado:
            qs = qs.filter(estado=estado)
        return qs