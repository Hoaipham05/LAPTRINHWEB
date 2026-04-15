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
from django.urls import path

from .views import (
    home_entry,
    user_login,
    user_register,
    user_logout,
    appointment_dashboard,
    consultation_dashboard,
    consultation_detail,
    customer_dashboard,
    customer_detail,
    customer_account,
    booking_page,
    feedback_dashboard,
    feedback_detail,
    service_dashboard,
    see_service,
    service_detail,
    customer_consultation_page,
    about_page,
    public_review_page,
)

urlpatterns = [
    path('', home_entry, name='home_entry'),
    path('login/', user_login, name='user_login'),
    path('register/', user_register, name='user_register'),
    path('logout/', user_logout, name='user_logout'),
    path('quan-ly/dich-vu/', service_dashboard, name='service_dashboard'),
    path('quan-ly/lich-hen/', appointment_dashboard, name='appointment_dashboard'),
    path('quan-ly/phan-hoi/', feedback_dashboard, name='feedback_dashboard'),
    path('quan-ly/phan-hoi/tu-van/', consultation_dashboard, name='consultation_dashboard'),
    path('quan-ly/phan-hoi/tu-van/<int:conversation_id>/', consultation_detail, name='consultation_detail'),
    path('quan-ly/phan-hoi/<int:feedback_id>/', feedback_detail, name='feedback_detail'),
    path('quan-ly/khach-hang/', customer_dashboard, name='customer_dashboard'),
    path('quan-ly/khach-hang/<int:customer_id>/', customer_detail, name='customer_detail'),
    path('tai-khoan/', customer_account, name='customer_account'),
    path('dat-lich/', booking_page, name='booking'),
    path('tu-van/', customer_consultation_page, name='customer_consultation'),
    path('services/', see_service, name='see_service'),
    path('services/<slug:slug>/', service_detail, name='service_detail'),
    path('gioi-thieu/', about_page, name='about_page'),
    path('danh-gia/', public_review_page, name='public_review_page'),

    # Legacy aliases kept for older templates/scripts.
    path('lich-hen/', appointment_dashboard),
    path('phan-hoi/', feedback_dashboard),
    path('phan-hoi/tu-van/', consultation_dashboard),
    path('phan-hoi/tu-van/<int:conversation_id>/', consultation_detail),
    path('phan-hoi/<int:feedback_id>/', feedback_detail),
    path('khach-hang/', customer_dashboard),
    path('khach-hang/<int:customer_id>/', customer_detail),

    path('admin/', admin.site.urls),
]
