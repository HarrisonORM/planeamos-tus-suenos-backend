from rest_framework.routers import DefaultRouter
from .views import ReservaViewSet

router = DefaultRouter()
router.register(
    "reservas",
    ReservaViewSet,
)

urlpatterns = router.urls