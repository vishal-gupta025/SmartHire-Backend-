from rest_framework.throttling import UserRateThrottle


class ResumeUploadThrottle(UserRateThrottle):
    scope = "resume_upload"
