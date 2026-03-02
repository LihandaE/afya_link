from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display =['email',
                   'first_name',
                   'last_name',
                   'role',
                   'hospital',
                   'is_staff',
                   'is_active',
                   ]
    list_filter = [
        'role',
        'hospital',
        'is_staff',
        'is_active',
    ]

    search_fields =['email', 'fist_name', 'last_name'
            ]
    
    fieldsets =(
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', { 'fields':('first_name', 'last_name', 'role', 'hospital')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
    
    )

    add_fieldsets= (
        (None, {
            "fields": ("email","first_name","last_name","role","hospital","password1","password2","is_staff","is_active",
            ),
        }),
    ),