from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('qr/', views.view_qr, name='qr'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='prepaid_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('history/', views.history, name='history'),
    path('topup/', views.topup, name='topup'),
]