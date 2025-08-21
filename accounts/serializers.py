from django.contrib.auth.models import User

from rest_framework import serializers

from .models import UserProfile


class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "headline",
            "summary",
            "contact_number",
            "education",
            "work_experience",
            "projects",
            "skills",
            "current_salary",
            "expected_salary",
            "notice_period",
            "primary_address",
            "secondary_address",
        ]


class CandidateSerializer(serializers.ModelSerializer):
    user_profile = CandidateProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "user_profile"]
        extra_kwargs = {"password": {"write_only": True}}
    

    def create(self, validated_data):
        """
        Creates user and user profile.
        """
        # Extract and remove user_profile from payload
        user_profile = validated_data.pop("user_profile")
        user_instance = super().create(validated_data) # Create a user entry first

        # Create UserProfile entry
        user_profile["user"] = user_instance
        UserProfile.objects.create(**user_profile)
        return user_instance
    
    def update(self, instance, validated_data):
        """
        Update user and user profile.
        """
        profile_data = validated_data.pop("user_profile", {})
        password = validated_data.pop("password", None)

        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()

        # Update UserProfile fields
        profile = instance.user_profile  # reverse relation
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance