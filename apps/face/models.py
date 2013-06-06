from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.OneToOneField(User, primary_key=True)
  certification = models.CharField(max_length=50)
  education = models.CharField(max_length=50)
  membership = models.CharField(max_length=50)
  experience_specialties = models.CharField(max_length=200)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
