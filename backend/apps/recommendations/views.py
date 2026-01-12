from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsCandidate
from apps.resumes.models import Resume
from apps.jobs.models import Job
from apps.accounts.models import RecruiterProfile
from apps.resumes.services.matching_engine import compute_match_score


class CandidateJobRecommendationsView(APIView):
    permission_classes = [IsCandidate]

    def get(self, request):
        user = request.user

        resume = Resume.objects.filter(
            candidate=user,
            is_parsed=True
        ).order_by("-updated_at").first()

        if not resume:
            return Response(
                {"detail": "Upload and parse a resume to get job recommendations"},
                status=400,
            )

        recommendations = []

        jobs = Job.objects.filter(is_active=True)

        for job in jobs:
            required_skills = [
                skill.strip()
                for skill in job.skills_required.split(",")
                if skill.strip()
            ]
            match_score, feedback = compute_match_score(
                resume_skills=resume.extracted_skills,
                job_required_skills=required_skills,
                job_optional_skills=[],
            )

            if match_score > 0:
                recruiter_profile = RecruiterProfile.objects.filter(
                user=job.recruiter
                ).first()
                recommendations.append({
                "job_id": job.id,
                "job_title": job.title,
                "company_name": (
                    recruiter_profile.company_name
                    if recruiter_profile else None
                ),
                "match_score": match_score,
                "match_feedback": feedback,
            })
            else :
                return Response(
                    {"detail": "No matching jobs found based on your resume."},
                    status=200,
                )

        recommendations.sort(
            key=lambda x: x["match_score"],
            reverse=True
        )

        return Response(recommendations)
