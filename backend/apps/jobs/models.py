from django.db import models
from apps.accounts.models import User


class Job(models.Model):
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    skills_required = models.TextField(
        help_text="Comma separated skills"
    )

    experience_required = models.PositiveIntegerField(
        help_text="Experience in years"
    )

    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()

    location = models.CharField(max_length=255)
    openings = models.PositiveIntegerField(default=1)

    ppo_offered = models.BooleanField(default=False)
    ppo_details = models.TextField(
        blank=True,
        null=True,
        help_text="Details about PPO eligibility, duration, stipend, etc."
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.recruiter.email}"
