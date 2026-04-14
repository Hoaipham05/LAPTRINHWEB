from django.urls import path
from . import views

urlpatterns = [
    path('dang-nhap/', views.login_view, name='login'),
    path('dang-ky/', views.signup_view, name='signup'),
    path('dang-xuat/', views.logout_view, name='logout'),
    path('ho-so/', views.profile_view, name='profile'),
]

