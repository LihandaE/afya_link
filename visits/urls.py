# visits/urls.py

from rest_framework.routers import DefaultRouter
from .views import VisitViewSet

router = DefaultRouter()
router.register(r"", VisitViewSet, basename="visits")

urlpatterns = router.urls