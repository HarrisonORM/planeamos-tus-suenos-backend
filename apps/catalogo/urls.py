from rest_framework.routers import DefaultRouter
from .views import (
    LocacionViewSet,
    PaqueteViewSet,
    ProductoAlquilerViewSet,
    ServicioPersonalViewSet,
)

router = DefaultRouter()
router.register(
    "productos",
    ProductoAlquilerViewSet,
)
router.register(
    "servicios",
    ServicioPersonalViewSet,
)
router.register(
    "paquetes",
    PaqueteViewSet,
)
router.register(
    "locaciones",
    LocacionViewSet,
)

urlpatterns = router.urls