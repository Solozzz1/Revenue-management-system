from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('tax_registration/', views.tax_registration, name='tax_registration'),
    path('revenue_management/', views.revenue_management, name='revenue_management'),
    path('accounts/', views.accounts, name='accounts'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # User Management
    path('manage_users/', views.manage_users, name='manage_users'),
    path('user/create/', views.user_create, name='user_create'),
    path('user/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('user/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    
    # Role Management
    path('manage_roles/', views.manage_roles, name='manage_roles'),
    path('role/create/', views.role_create, name='role_create'),
    path('role/edit/<int:role_id>/', views.role_edit, name='role_edit'),
    path('role/delete/<int:role_id>/', views.role_delete, name='role_delete'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

]
