"""
URL configuration for SPA project.

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
from django.views.generic import TemplateView

from .views import (
    appointment_dashboard,
    booking,
    consultation_page,
    consultation_dashboard,
    consultation_detail,
    customer_dashboard,
    customer_detail,
    feedback_dashboard,
    feedback_detail,
    service_dashboard,
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dich-vu/', service_dashboard, name='service_dashboard'),
    path('tu-van/', consultation_page, name='consultation_page'),
    path('dat-lich/', booking, name='booking'),
    path('phan-hoi/', feedback_dashboard, name='feedback_dashboard'),
    path('phan-hoi/tu-van/', consultation_dashboard, name='consultation_dashboard'),
    path('phan-hoi/tu-van/<int:conversation_id>/', consultation_detail, name='consultation_detail'),
    path('phan-hoi/<int:feedback_id>/', feedback_detail, name='feedback_detail'),
    path('khach-hang/', customer_dashboard, name='customer_dashboard'),
    path('khach-hang/<int:customer_id>/', customer_detail, name='customer_detail'),
    path('auth/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
