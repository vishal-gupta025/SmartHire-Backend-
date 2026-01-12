from django.urls import path
from .views import RecruiterTestView
from rest_framework.routers import DefaultRouter
from .views import JobViewSet

urlpatterns = [
    path("recruiter-test/", RecruiterTestView.as_view()),
]

router = DefaultRouter()
router.register(r"", JobViewSet, basename="jobs")

urlpatterns += router.urls