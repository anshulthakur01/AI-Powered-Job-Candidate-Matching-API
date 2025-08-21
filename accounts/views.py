from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import CandidateSerializer
from core.utils.auth import ProtectedView

# Create your views here.
class CandidateListCreate(ProtectedView, ListCreateAPIView):
    queryset = User.objects.exclude(is_superuser=True).select_related("user_profile").all().order_by('-date_joined')
    serializer_class = CandidateSerializer


class CandidateRetrieveUpdateDestroyView(ProtectedView, RetrieveUpdateDestroyAPIView):
    queryset = User.objects.select_related("user_profile").all()
    serializer_class = CandidateSerializer