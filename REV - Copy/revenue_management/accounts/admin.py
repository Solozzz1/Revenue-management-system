# admin.py
from django.contrib import admin
from .models import User, Role

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    filter_horizontal = ('roles',)  # Provides a widget for selecting roles

# Register the models with the admin site
admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)
