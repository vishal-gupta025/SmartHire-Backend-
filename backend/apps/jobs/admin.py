from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "recruiter",
        "location",
        "experience_required",
        "salary_min",
        "salary_max",
        "ppo_offered",
        "is_active",
        "created_at",
    )
    list_filter = ("location", "is_active", "experience_required", "ppo_offered",)
    search_fields = ("title", "skills_required", "description", "ppo_details")
