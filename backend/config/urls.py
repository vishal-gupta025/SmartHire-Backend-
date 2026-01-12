from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.accounts.views import CustomTokenObtainPairView
from apps.accounts.views import ProtectedView
from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api/test/protected/", ProtectedView.as_view()),
    path("api/jobs/", include("apps.jobs.urls")),
    path("api/applications/", include("apps.applications.urls")),
    path("api/resumes/", include("apps.resumes.urls")),
    path("api/recommendations/", include("apps.recommendations.urls")),

]