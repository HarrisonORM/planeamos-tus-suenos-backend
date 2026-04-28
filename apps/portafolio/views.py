from rest_framework import viewsets
from .models import EventoPortafolio
from .serializers import EventoPortafolioSerializer


class EventoPortafolioViewSet(viewsets.ModelViewSet):
    queryset = EventoPortafolio.objects.all()
    serializer_class = EventoPortafolioSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        tipo = self.request.query_params.get(
            "tipo_evento"
        )
        if tipo:
            qs = qs.filter(tipo_evento=tipo)
        return qs