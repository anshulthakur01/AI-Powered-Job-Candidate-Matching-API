from django.db import models
from django.contrib.auth.models import User

from core.models import TimeStamp

# Create your models here.
class UserProfile(TimeStamp):
    headline = models.CharField(max_length=255)
    summary = models.TextField(max_length=1000)
    contact_number = models.CharField(max_length=15)
    education = models.JSONField(default=list)
    work_experience = models.FloatField()
    projects = models.JSONField(default=list)
    skills = models.JSONField(default=list)
    current_salary = models.PositiveIntegerField(help_text="Current Yearly salary")
    expected_salary = models.PositiveIntegerField(help_text="Expected Yearly salary")
    notice_period = models.PositiveIntegerField()
    primary_address = models.TextField()
    secondary_address = models.TextField()
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.headline} ({self.user.username})"