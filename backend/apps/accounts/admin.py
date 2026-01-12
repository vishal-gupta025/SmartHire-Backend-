from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, CandidateProfile, RecruiterProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "role")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "role", "is_active", "is_staff", "is_superuser")

# class CandidateProfileInline(admin.StackedInline):
#     model = CandidateProfile
#     can_delete = False
#     extra = 0


# class RecruiterProfileInline(admin.StackedInline):
#     model = RecruiterProfile
#     can_delete = False
#     extra = 0



class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")

    # inlines = [CandidateProfileInline, RecruiterProfileInline]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Role", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "is_active", "is_staff"),
        }),
    )

    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdmin)

admin.site.register(CandidateProfile)
admin.site.register(RecruiterProfile)