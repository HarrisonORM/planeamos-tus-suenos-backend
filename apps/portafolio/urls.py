from rest_framework.routers import DefaultRouter
from .views import EventoPortafolioViewSet

router = DefaultRouter()
router.register(
    "eventos",
    EventoPortafolioViewSet,
)

urlpatterns = router.urls