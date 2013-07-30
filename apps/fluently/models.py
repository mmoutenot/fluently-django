from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Therapy Need Choices

# 1 - Articualtion
# 2 - Stuttering
# 3 - Apraxia of Speech
# 4 - Dysarthria
# 5 - Aphasia
# 6 - Autism-Spectrum Disorder
# 7 - Asperger Syndrome
# 8 - Communication Disorder
# 9 - Dyslexia
# 10 - Augmentative & Alternative Communication (AAC)
# 11 - Accent Modification
# 12 - Developmental Delay
# 13 - Dysphagia
# 14 - Other

THERAPY_NEED_CHOICES = (
    (1, 'articulation'), 
    (2, 'stuttering'),   
    (3, 'apraxia'),
    (4, 'dysarthria'),
    (5, 'aphasia'),
    (6, 'autism'),
    (7, 'asperger'),
    (8, 'commdisorder'),
    (9, 'dyslexia'),
    (10, 'aac'),
    (11, 'accent'),
    (12, 'devdelay'),
    (13, 'dysphagia'),
    (14, 'other'),
)

# Located In Choices

# N - No Preference
# O - Office or Clinic
# H - Home
# V - Online or Videoconferencing

LOCATED_IN_CHOICES = (
    ('N', 'no-preference'),
    ('O', 'office'),
    ('H', 'home'),
    ('V', 'online'),
)

# Payment Method Choices

# N - No Preference
# H - Hourly Rate (Cash/Credit)
# I - Accepts Insurance

PAYMENT_METHOD_CHOICES = (
    ('N', 'no-preference'),
    ('H', 'hourly'),
    ('I', 'insurance'),
)

class SearchQuery(models.Model):
    
    need = models.CharField(max_length=2, choices=THERAPY_NEED_CHOICES)
    zip_code = models.CharField(max_length=9)
    located_in = models.CharField(max_length=1, choices=LOCATED_IN_CHOICES)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD_CHOICES)

class StudentRequest(models.Model):

    REQUEST_TYPE_CHOICES = (
        ('G', 'General'),
        ('S', 'SpecificTherapist'),
    )

    email = models.CharField(max_length=30)
    name = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=9)
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
    zip_code = models.CharField(max_length=9)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=100)
    specialties = models.CharField(max_length=512)
    specialties_list = models.CommaSeparatedIntegerField(max_length=14) # Therapy Need Choices e.g. "1, 2, 10"
    located_in = models.CommaSeparatedIntegerField(max_length=7)
    payment_method = models.CommaSeparatedIntegerField(max_length=4)
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
