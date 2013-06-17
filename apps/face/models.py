from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.OneToOneField(User, primary_key=True)
  join_id = models.CharField(max_length=36, unique=True)
  confirmed = models.BooleanField(default=False)

  def __str__(self):
    return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
  if created:
    profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
