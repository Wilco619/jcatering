from django.urls import path
from . import views

app_name = 'japp'  # Namespace for the app

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu, name='menu'),
    path('gallery/', views.gallery, name='gallery'),
    path('request-callback/', views.request_callback, name='request_callback'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('quote-request/', views.quote_request_view, name='quote_request'),
    # Admin URLs
    path('custom-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('custom-admin/menu/', views.admin_menu, name='admin_menu'),
    path('custom-admin/menu/add/', views.admin_menu_add, name='admin_menu_add'),
    path('custom-admin/menu/edit/<int:pk>/', views.admin_menu_edit, name='admin_menu_edit'),
    path('custom-admin/menu/delete/<int:pk>/', views.admin_menu_delete, name='admin_menu_delete'),
    
    path('custom-admin/gallery/', views.admin_gallery, name='admin_gallery'),
    path('custom-admin/gallery/add/', views.admin_gallery_add, name='admin_gallery_add'),
    path('custom-admin/gallery/edit/<int:pk>/', views.admin_gallery_edit, name='admin_gallery_edit'),
    path('custom-admin/gallery/delete/<int:pk>/', views.admin_gallery_delete, name='admin_gallery_delete'),
    
    path('custom-admin/quotes/', views.admin_quotes, name='admin_quotes'),
    path('custom-admin/quotes/<int:pk>/', views.admin_quote_detail, name='admin_quote_detail'),
    path('custom-admin/quotes/<int:pk>/update-status/', views.admin_quote_update_status, name='admin_quote_update_status'),
    
    path('custom-admin/contacts/', views.admin_contacts, name='admin_contacts'),
    path('custom-admin/contacts/<int:pk>/', views.admin_contact_detail, name='admin_contact_detail'),
    path('custom-admin/contacts/<int:pk>/mark-read/', views.admin_contact_mark_read, name='admin_contact_mark_read'),
    
    path('custom-admin/subscribers/', views.admin_subscribers, name='admin_subscribers'),
    path('custom-admin/subscribers/export/', views.admin_subscribers_export, name='admin_subscribers_export'),
]