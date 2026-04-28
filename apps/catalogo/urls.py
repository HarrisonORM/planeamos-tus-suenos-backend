from rest_framework.routers import DefaultRouter
from .views import (
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

urlpatterns = router.urls