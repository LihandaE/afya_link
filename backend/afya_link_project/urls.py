"""
URL configuration for afya_link_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/auth/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name= 'token_refresh'),

    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/hospitals/", include("hospitals.urls")),
    path("api/v1/doctors/", include("doctors.urls")),
    path("api/v1/patients/", include("patients.urls")),
    path("api/v1/appointments/", include("appointments.urls")),
    path("api/v1/records/", include("records.urls")),
    path("api/v1/consent/", include("consent.urls")),
    path("api/v1/visits/", include("visits.urls")),

]
