from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, CandidateProfile, RecruiterProfile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        token["role"] = user.role

        return token
    

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)
    role = serializers.ChoiceField(
    choices=[User.Role.CANDIDATE, User.Role.RECRUITER]
    )

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already registered")
        return email
    
    def create(self, validated_data):
        role = validated_data["role"]
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role=role
        )
        if role == User.Role.CANDIDATE:
            CandidateProfile.objects.create(
                user=user,
                name=validated_data.get("name", "")
            )
        elif role == User.Role.RECRUITER:
            RecruiterProfile.objects.create(
                user=user,
                company_name=validated_data.get("name", "")
            )
        return user