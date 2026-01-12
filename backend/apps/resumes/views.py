from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from apps.accounts.permissions import IsCandidate
from .models import Resume
from .serializers import ResumeUploadSerializer
from .throttles import ResumeUploadThrottle
from .services.text_extractor import extract_resume_text
from .services.ats_scoring import compute_ats_score
from .tasks import parse_resume_task

class CandidateTestView(APIView):
    permission_classes = [IsCandidate]

    def get(self, request):
        return Response({
            "message": "Candidate access granted",
            "email": request.user.email,
            "role": request.user.role
        })


class ResumeUploadView(APIView):
    permission_classes = [IsCandidate]
    throttle_classes = [ResumeUploadThrottle]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = serializer.validated_data["file"]

        resume = Resume.objects.create(
            candidate=request.user,
            file=file,
            original_filename=file.name,
        )
    
        parse_resume_task.delay(resume.id)

        return Response(
            {
                "id": resume.id,
                "message": "Resume uploaded successfully",
            },
            status=status.HTTP_201_CREATED,
        )
    

class ResumeParseView(APIView):
    permission_classes = [IsCandidate]

    def post(self, request, resume_id):
        user = request.user

        try:
            resume = Resume.objects.get(id=resume_id, candidate=user)
        except Resume.DoesNotExist:
            return Response(
                {"detail": "Resume not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        if resume.is_parsed:
            return Response(
                {"detail": "Resume already parsed"},
                status=status.HTTP_400_BAD_REQUEST,
            )        

        try:
            text = extract_resume_text(resume.file.path)

            ats_score, feedback = compute_ats_score(text)

            resume.ats_score = ats_score
            resume.ats_feedback = feedback
            resume.extracted_text = text
            resume.is_parsed = True
            resume.parse_error = None
            resume.save()

            return Response(
                {"message": "Resume parsed successfully"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            resume.parse_error = str(e)
            resume.is_parsed = False
            resume.save()

            return Response(
                {"detail": "Failed to parse resume"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )