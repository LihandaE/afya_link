# records/urls.py

from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"labs", LabRecordViewSet)
router.register(r"radiology", RadiologyRecordViewSet)
router.register(r"diagnoses", DiagnosisViewSet)
router.register(r"prescriptions", PrescriptionViewSet)

urlpatterns = router.urls