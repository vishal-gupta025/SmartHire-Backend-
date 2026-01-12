from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "candidate",
        "original_filename",
        "is_parsed",
        "uploaded_at",
    )
    list_filter = ("is_parsed",)
    search_fields = ("candidate__email",)
