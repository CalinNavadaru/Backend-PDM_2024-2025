"""
URL configuration for backend_pdm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from backend_app.views import Register
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('api/employees/', include("backend_app.urls")),
    # Endpoint pentru obținerea token-ului de acces
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint pentru verificarea token-ului de refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Endpoint pentru verificarea token-ului de acces
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Endpoint pentru inregistrare
    path('api/register/', Register.as_view(), name="token_register"),

]
