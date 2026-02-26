from rest_framework.routers import DefaultRouter
from .views import DoctorViewset, SpecialityViewset

router =DefaultRouter()
router.register(r"doctors", DoctorViewset)
router.register(r"specialities", SpecialityViewset)

urlpatterns= router.urls