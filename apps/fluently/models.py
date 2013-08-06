from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Role Choices

# 1 - Speech-Language Pathologist
# 2 - Audiologist

ROLE_CHOICES = {
    (1, 'slp'),
    (2, 'aud'),
}

# Certification Choices

# 1 - CCC-SLP
# 2 - MA
# 3 - MS
# 4 - M.Ed
# 5 - Ph.D
# 6 - BRS-FD
# 7 - BRS-S
# 8 - BRS-CL

CERTIFICATION_CHOICES = (
    (1, 'ccc'),
    (2, 'marts'),
    (3, 'mscience'),
    (4, 'medu'),
    (5, 'phd'),
    (6, 'fluencydisorders'),
    (7, 'swallowing'),
    (8, 'childlang'),
)

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

SPECIALTY_CHOICES = (
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

# Age Choices

# 1 - 0-4 - child
# 2 - 5-10 - elementary
# 3 - 11-17 - teen
# 4 - 18-65 - adult
# 5 - 66+ - senior

CLIENT_AGE_CHOICES = (
    (1, 'child'),
    (2, 'elementary'),
    (3, 'teen'),
    (4, 'adult'),
    (5, 'senior'),
)

# Located In Choices

# 1 - No Preference
# 2 - Office or Clinic
# 3 - Home
# 4 - Online or Videoconferencing

LOCATED_IN_CHOICES = (
    (1, 'no-preference'),
    (2, 'office'),
    (3, 'home'),
    (4, 'online'),
)

# Payment Method Choices

# 1 - No Preference
# 2 - Hourly Rate (Cash/Credit)
# 3 - Accepts Insurance

PAYMENT_METHOD_CHOICES = (
    (1, 'no-preference'),
    (2, 'hourly'),
    (3, 'insurance'),
)

class SearchQuery(models.Model):
    
    need = models.CharField(max_length=2, choices=SPECIALTY_CHOICES)
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

    about_me = models.CharField(max_length=300)
    certifications = models.CharField(max_length=300)
    certification_list = models.CommaSeparatedIntegerField(max_length=30)
    city = models.CharField(max_length=100)
    client_ages_list = models.CommaSeparatedIntegerField(max_length=18)
    confirmed = models.BooleanField(default=False)
    country = models.CharField(max_length=100)
    emailed = models.BooleanField(default=False)
    experience = models.CharField(max_length=300)
    first_name = models.CharField(max_length=64)
    join_id = models.CharField(max_length=36, unique=True)
    last_name = models.CharField(max_length=64)
    located_in = models.CommaSeparatedIntegerField(max_length=7)
    name = models.CharField(max_length=64)
    needs = models.CharField(max_length=512)
    payment_method = models.CommaSeparatedIntegerField(max_length=4)
    phone = models.CharField(max_length=36)
    pic_url = models.CharField(max_length=512)
    role = models.CharField(max_length=1)
    specialties = models.CharField(max_length=512)
    specialties_list = models.CommaSeparatedIntegerField(max_length=22)
    state = models.CharField(max_length=2)
    therapy_approach = models.CharField(max_length=300)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)
    user_url = models.CharField(max_length=6, unique=True)
    viewed_account = models.BooleanField(default=False)
    zip_code = models.CharField(max_length=9)

    def __str__(self):
        return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
