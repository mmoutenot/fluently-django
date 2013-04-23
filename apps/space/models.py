from django.db import models
from django_extensions.db.fields import UUIDField

class Space(models.Model):
  url_id         = UUIDField(version=4)
  tok_session_id = models.CharField(max_length=255)
