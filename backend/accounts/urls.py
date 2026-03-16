from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UserViewSet, LoginView

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
]

urlpatterns += router.urls