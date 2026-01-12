from django.db import models
from apps.accounts.models import User


class Resume(models.Model):
    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resumes"
    )

    file = models.FileField(upload_to="resumes/")
    original_filename = models.CharField(max_length=255)

    extracted_text = models.TextField(blank=True, null=True)

    extracted_skills = models.JSONField(
        null=True,
        blank=True,
    )

    ats_score = models.FloatField(default=0.0)
    ats_feedback = models.JSONField(blank=True, null=True)

    is_parsed = models.BooleanField(default=False)
    parse_error = models.TextField(blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate.email} - Resume"
