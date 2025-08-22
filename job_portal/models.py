from django.db import models
from django.contrib.auth.models import User

from core.models import TimeStamp
from core.utils.enums import EMPLOYMENT_TYPE_CHOICES, JOB_APPLICATION_STATUS_CHOICES

# Create your models here.
class Company(TimeStamp):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.TextField()
    website = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Job(TimeStamp):
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Skills & Requirements
    required_skills = models.JSONField(default=list)
    preferred_skills = models.JSONField(default=list)
    experience_required = models.PositiveIntegerField(blank=True, null=True)
    education_required = models.JSONField(default=list)

    employment_type = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default="full_time"
    )
    deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, related_name="jobs", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class JobApplication(TimeStamp):
    user = models.ForeignKey(User, related_name="job_applications", on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name="applications", on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=50, choices=JOB_APPLICATION_STATUS_CHOICES, default="applied")

    class Meta:
        unique_together = ("user", "job")  # prevent duplicate applications

    def __str__(self):
        return f"{self.user}, {self.job}, ({self.status})"