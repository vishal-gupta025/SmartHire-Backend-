from rest_framework import serializers
from .models import Application



class ApplicationSerializer(serializers.ModelSerializer):
    candidate = serializers.ReadOnlyField(source="candidate.email")
    job = serializers.ReadOnlyField(source="job.id")

    class Meta:
        model = Application
        fields = (
            "id",
            "candidate",
            "job",
            "status",
            "ats_score",
            "ats_feedback",
            "applied_at",
        )
        read_only_fields = ("status", "applied_at")

class RecruiterApplicationSerializer(serializers.ModelSerializer):
    candidate_email = serializers.ReadOnlyField(source="candidate.email")
    job_title = serializers.ReadOnlyField(source="job.title")

    class Meta:
        model = Application
        fields = (
            "id",
            "candidate_email",
            "job_title",
            "status",
            "ats_score",       
            "ats_feedback",
            "applied_at",
        )