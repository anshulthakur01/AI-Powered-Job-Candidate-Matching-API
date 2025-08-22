from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer
from core.utils.auth import ProtectedView
from core.utils.llm_utils import grok_client

# Create your views here.
class JobListCreateView(ProtectedView, ListCreateAPIView):
    queryset = Job.objects.select_related('company').all()
    serializer_class = JobSerializer


class JobRetrieveUpdateDestroyView(ProtectedView, RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.select_related("company").all()
    serializer_class = JobSerializer

class JobApplicationListCreateView(ProtectedView, ListCreateAPIView):
    queryset = JobApplication.objects.select_related('job', 'user').all()
    serializer_class = JobApplicationSerializer

class RecommendedJobsView(ProtectedView, ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        """
        Return recommended jobs for the authenticated user.
        """

        qs = Job.objects.filter(is_active=True).select_related("company")

        user_profile = getattr(self.request.user, "user_profile", None)
        if user_profile and user_profile.skills:
            # Find commond skills user and job
            qs = [job for job in qs if set(job.required_skills+job.preferred_skills).intersection(user_profile.skills)]

        return qs


class AiPoweredTopCandidatesView(ProtectedView, APIView):
    serializer_class = JobApplicationSerializer

    def get(self, request, job_id):

        job_applications = JobApplication.objects.select_related('user', 'job', 'user__user_profile').filter(job_id=job_id)

        job = job_applications.first().job

        jd = {
            "title": job.title,
            "description": job.description,
            "required_skills": job.required_skills,
            "preferred_skills": job.preferred_skills,
            "experience_required": job.experience_required,
            "education_required": job.education_required,
            "employment_type": job.employment_type
        }

        print("JD :", jd)

        # Collect users data from the Applid jobs
        user_data = [
            {
                "user_profile_id": ja.user.user_profile.id,
                "headline": ja.user.user_profile.headline,
                "summary": ja.user.user_profile.summary,
                "work_experience": ja.user.user_profile.work_experience,
                "education": ja.user.user_profile.education,
                "projects": ja.user.user_profile.projects,
                "skills": ja.user.user_profile.skills,

            }
            for ja in job_applications
            if hasattr(ja.user, "user_profile")
        ]

        print("User data:", user_data)

        llm_response = grok_client.process_candidate_ranking(jd, user_data)

        return Response(llm_response, status=status.HTTP_200_OK)