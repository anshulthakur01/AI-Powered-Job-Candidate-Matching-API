from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Job, Company, JobApplication


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)  # input only
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = fields = [
            "title",
            "description",
            "required_skills",
            "preferred_skills",
            "experience_required",
            "education_required",
            "employment_type",
            "deadline",
            "is_active",
            "company",
            "company_name"
        ]

    def create(self, validated_data):
        company_name = validated_data.pop('company_name')

        # Assign existing company with name or create new company if does not exist
        validated_data['company'], is_created = Company.objects.get_or_create(name=company_name)
        return super().create(validated_data)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"