from django.db import models
from apps.accounts.models import User
from apps.jobs.models import Job


class Application(models.Model):
    STATUS_CHOICES = (
        ("APPLIED", "Applied"),
        ("SHORTLISTED", "Shortlisted"),
        ("REJECTED", "Rejected"),
        ("HIRED", "Hired"),
    )

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    ats_score = models.FloatField(default=0.0)
    ats_feedback = models.JSONField(default=dict)

    match_score = models.FloatField(default=0.0)
    match_feedback = models.JSONField(blank=True, null=True)


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="APPLIED"
    )

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("candidate", "job")

    def __str__(self):
        return f"{self.candidate.email} → {self.job.title}"
