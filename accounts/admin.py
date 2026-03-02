from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import UserCreationForm, UserChangeForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    ordering = ("email",)

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "hospital",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "hospital",
        "is_staff",
        "is_active",
    )

    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),

        (_("Personal Info"), {
            "fields": ("first_name", "last_name", "role", "hospital")
        }),

        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),

        (_("Important Dates"), {
            "fields": ("last_login",),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "role",
                "hospital",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )


admin.site.register(User, UserAdmin)