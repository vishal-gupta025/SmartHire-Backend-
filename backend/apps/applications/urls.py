from django.urls import path
from .views import (
    ApplyToJobView,
    RecruiterApplicationsView,
    RecruiterJobApplicationsView,
    UpdateApplicationStatusView,
)

urlpatterns = [
    # Candidate applies to a job
    path(
        "jobs/<int:job_id>/apply/",
        ApplyToJobView.as_view(),
        name="apply-to-job",
    ),

    # Recruiter dashboard (all applications across jobs)
    path(
        "recruiter/",
        RecruiterApplicationsView.as_view(),
        name="recruiter-applications",
    ),

    # recruiter views ranked applications for ONE job
    path(
        "jobs/<int:job_id>/applications/",
        RecruiterJobApplicationsView.as_view(),
        name="recruiter-job-applications",
    ),

    # Recruiter updates application status
    path(
        "<int:application_id>/status/",
        UpdateApplicationStatusView.as_view(),
        name="update-application-status",
    ),

    path(
    "jobs/<int:job_id>/ranked/",
    RecruiterJobApplicationsView.as_view(),
    ),
]
