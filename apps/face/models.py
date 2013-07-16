from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class StudentRequest(models.Model):
    REQUEST_TYPE_CHOICES = (
        ('G', 'General'),
        ('S', 'SpecificTherapist'),
    )

    email = models.CharField(max_length=30)
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=32)
    needs = models.CharField(max_length=512)
    slp = models.CharField(max_length=30)
    requestType = models.CharField(max_length=1, choices=REQUEST_TYPE_CHOICES)

    def __str__(self):
        return "Request from %s" % self.email

class UserProfile(models.Model):

    USER_TYPE_CHOICES = (
        ('P', 'Provider'),
        ('S', 'Student'),
    )

    user = models.OneToOneField(User, primary_key=True)
    user_url = models.CharField(max_length=6, unique=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=36)
    name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    about_me = models.CharField(max_length=300)
    certifications = models.CharField(max_length=300)
    experience = models.CharField(max_length=300)
    therapy_approach = models.CharField(max_length=300)
    location = models.CharField(max_length=32)
    specialties = models.CharField(max_length=512)
    needs = models.CharField(max_length=512)
    join_id = models.CharField(max_length=36, unique=True)
    pic_url = models.CharField(max_length=512)
    confirmed = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False)

    def __str__(self):
        return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
