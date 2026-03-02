from rest_framework.routers import DefaultRouter
from .views import PatientProfileViewSet

router = DefaultRouter()
router.register("", PatientProfileViewSet)

urlpatterns = router.urls

