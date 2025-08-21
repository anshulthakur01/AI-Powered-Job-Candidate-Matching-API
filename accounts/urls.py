from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CandidateListCreate, CandidateRetrieveUpdateDestroyView

urlpatterns = [
    # Authentication and Auth urls
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),  

    # User related urls
    path('candidates', CandidateListCreate.as_view(), name='candidates_list_create'),
    path('candidates/<int:pk>', CandidateRetrieveUpdateDestroyView.as_view(), name='candidate_detail_update_delete'),
]