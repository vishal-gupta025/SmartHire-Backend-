from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.permissions import IsCandidate, IsRecruiter
from apps.jobs.models import Job
from .models import Application
from .serializers import ApplicationSerializer, RecruiterApplicationSerializer
from .throttles import JobApplyThrottle
from apps.resumes.models import Resume
from apps.resumes.services.ats_scoring import calculate_job_ats_score
from django.shortcuts import get_object_or_404
from apps.resumes.services.matching_engine import compute_match_score


class ApplyToJobView(APIView):
    permission_classes = [IsCandidate]
    throttle_classes = [JobApplyThrottle]

    def post(self, request, job_id):
        user = request.user

        try:
            job = Job.objects.get(id=job_id, is_active=True)
        except Job.DoesNotExist:
            return Response(
                {"detail": "Job not found or inactive"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if Application.objects.filter(candidate=user, job=job).exists():
            return Response(
                {"detail": "You have already applied to this job"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        resume = (
            Resume.objects.filter(candidate=user, is_parsed=True)
            .order_by("-updated_at")
            .first()
        )

        if not resume:
            return Response(
                {"detail": "Please upload and parse a resume before applying"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure resume skills are a dict for downstream services
        resume_skills = resume.extracted_skills or {}

        job_skills = [
            skill.strip()
            for skill in job.skills_required.split(",")
            if skill.strip()
        ]

        ats_score, ats_feedback = calculate_job_ats_score(
            resume_skills=resume_skills,
            job_skills=job_skills or [],
            base_resume_score=resume.ats_score,
        )

        match_score, match_feedback = compute_match_score(
            resume_skills=resume_skills,
            job_required_skills=job_skills or [],
            job_optional_skills=[],
        )


        application = Application.objects.create(
            candidate=user,
            job=job,
            ats_score=ats_score,
            ats_feedback=ats_feedback,
            match_score = match_score,
            match_feedback = match_feedback
        )

        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecruiterApplicationsView(APIView):
    permission_classes = [IsRecruiter]

    def get(self, request):
        recruiter = request.user

        applications = Application.objects.filter(
            job__recruiter=recruiter
        ).select_related("candidate", "job")

        serializer = RecruiterApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    

class UpdateApplicationStatusView(APIView):
    permission_classes = [IsRecruiter]

    def patch(self, request, application_id):
        recruiter = request.user
        new_status = request.data.get("status")

        if new_status not in ["SHORTLISTED", "REJECTED", "HIRED"]:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            application = Application.objects.get(id=application_id, job__recruiter=recruiter)
        except Application.DoesNotExist:
            return Response({"detail": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

        application.status = new_status
        application.save()

        return Response({"detail": f"Application marked as {new_status}"}, status=status.HTTP_200_OK)


class RecruiterJobApplicationsView(APIView):
    permission_classes = [IsRecruiter]

    def get(self, request, job_id):
        # enforce recruiter owns the job and return ranked applications
        job = get_object_or_404(Job, id=job_id, recruiter=request.user)

        applications = (
            Application.objects
            .filter(job=job)
            .select_related("candidate", "job")
            .order_by("-match_score", "-ats_score", "-applied_at")
        )

        serializer = RecruiterApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)