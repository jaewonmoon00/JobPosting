from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BaseUser(User):
    verified = models.BooleanField(default=False)

class EmployerUser(BaseUser):
    documents_authenticated = models.BooleanField(default=False)
    verification_in_progress = models.BooleanField(default=False)
    public_key = models.TextField()

class ApplicantUser(BaseUser):
    pass
