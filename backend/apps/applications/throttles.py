from rest_framework.throttling import UserRateThrottle


class JobApplyThrottle(UserRateThrottle):
    scope = "job_apply"
