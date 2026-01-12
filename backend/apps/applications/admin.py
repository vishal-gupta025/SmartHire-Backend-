from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "candidate",
        "job",
        "status",
        "ats_score",
        "applied_at",
    )
    list_filter = ("status", "applied_at")
    search_fields = ("candidate__email", "job__title")
    ordering = ("-applied_at",)
