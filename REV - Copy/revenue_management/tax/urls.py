from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    # Invoice-related URLs
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/pay/', views.process_payment, name='process_payment'),
    path('generate-bill/', views.generate_bill, name='generate_bill'),

    # Admin-side URLs for managing tax types
    path('manage-tax-types/', views.manage_tax_types, name='manage_tax_types'),
    path('create-tax-type/', views.create_tax_type, name='create_tax_type'),
    path('edit-tax-type/<int:tax_type_id>/', views.edit_tax_type, name='edit_tax_type'),    
    path('delete-tax-type/<int:tax_type_id>/', views.delete_tax_type, name='delete_tax_type'),

    # Admin-side URLs for managing invoices
    path('manage-invoices/', views.manage_invoices, name='manage_invoices'),
    path('revenue-reports/', views.revenue_report, name='revenue_reports'),

    # Taxpayer Registration URLs
    path('register-individual/', views.register_individual_taxpayer, name='register_individual'),
    path('register-business/', views.register_business_taxpayer, name='register_business'),

    # Taxpayer profile URLs
    path('taxpayer/profile/<str:identifier>/', views.taxpayer_profile_view, name='taxpayer_profile_view'),
    path('taxpayer/profile/edit/', views.edit_taxpayer_profile, name='edit_taxpayer_profile'),
    path('taxpayer/history/', views.taxpayer_history, name='taxpayer_history'),

    # Password management URLs
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Category management URLs
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # Bill Type management URLs
    path('bill_types/', views.manage_bill_types, name='manage_bill_types'),
    path('bill_types/create/', views.bill_type_create, name='bill_type_create'),
    path('bill_types/edit/<int:pk>/', views.bill_type_edit, name='bill_type_edit'),
    path('bill_types/delete/<int:pk>/', views.bill_type_delete, name='bill_type_delete'),

    # taxpayer managementurls 
    path('taxpayer/add/', views.taxpayer_add, name='taxpayer_add'),
    path('taxpayer/edit/<str:id_number>/', views.taxpayer_edit, name='taxpayer_edit'),
    path('taxpayer/delete/<str:id_number>/', views.taxpayer_delete, name='taxpayer_delete'),
    path('taxpayer/profile/<str:identifier>/', views.taxpayer_profile_view, name='taxpayer_profile_view'),


    # Registration URLs
    path('register/individual/', views.individual_register, name='individual_register'),
    path('register/business/', views.business_register, name='business_register'),

]
