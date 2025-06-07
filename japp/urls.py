from django.urls import path
from . import views

app_name = 'japp'  # Namespace for the app

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu, name='menu'),
    path('gallery/', views.gallery, name='gallery'),
    path('request-callback/', views.request_callback, name='request_callback'),
    path('subscribe/', views.subscribe, name='subscribe'),
]