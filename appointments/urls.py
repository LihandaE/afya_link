from rest_framework.routers import DefaultRouter
from .views import AppointmentViewset

router= DefaultRouter()
router.register(r"",AppointmentViewset, basename="appointments")

urlpatterns= router.urls
