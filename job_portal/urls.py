from django.urls import path

from .views import JobListCreateView, JobApplicationListCreateView, JobRetrieveUpdateDestroyView, RecommendedJobsView, AiPoweredTopCandidatesView

urlpatterns = [
    path('jobs', JobListCreateView.as_view(), name='job_list_create'),
    path('job-applications', JobApplicationListCreateView.as_view(), name='job_application_list_create'),
    path('jobs/recommended', RecommendedJobsView.as_view(), name='recommended_job_list'),
    path('jobs/<int:pk>', JobRetrieveUpdateDestroyView.as_view(), name='job_detail_update_delete'),
    path('jobs/<int:job_id>/top-candidates', AiPoweredTopCandidatesView.as_view(), name='ai_powered_top_candidates'),
]
