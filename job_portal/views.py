from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer
from core.utils.auth import ProtectedView

# Create your views here.
class JobListCreateView(ProtectedView, ListCreateAPIView):
    queryset = Job.objects.select_related('company').all()
    serializer_class = JobSerializer


class JobRetrieveUpdateDestroyView(ProtectedView, RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.select_related("company").all()
    serializer_class = JobSerializer

class JobApplicationListCreatetView(ProtectedView, ListCreateAPIView):
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