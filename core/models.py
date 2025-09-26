from django.db import models
from django.contrib.auth.models import User

# Extend user profile later for extra fields
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Extra fields can be added later
    dream_role = models.CharField(max_length=100, blank=True, null=True)
    current_skills = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.username
