from rest_framework.routers import DefaultRouter
from .views import (
    MensajeContactoViewSet,
    CotizacionViewSet,
)

router = DefaultRouter()
router.register(
    "mensajes",
    MensajeContactoViewSet,
)
router.register(
    "cotizaciones",
    CotizacionViewSet,
)

urlpatterns = router.urls