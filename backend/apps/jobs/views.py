from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.accounts.permissions import IsRecruiter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsRecruiter
from .models import Job
from .serializers import JobSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class RecruiterTestView(APIView):
    permission_classes = [IsRecruiter]

    def get(self, request):
        return Response({
            "message": "Recruiter access granted",
            "email": request.user.email,
            "role": request.user.role
        })


class JobViewSet(ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = [
        "location",
        "experience_required",
        "is_active",
        "ppo_offered",
    ]

    search_fields = [
        "title",
        "description",
        "skills_required",
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == "RECRUITER":
            return Job.objects.filter(recruiter=user)

        return Job.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsRecruiter()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)