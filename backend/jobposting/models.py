from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from user_management.models import BaseUser, EmployerUser, ApplicantUser, User
from profiles.models import ApplicantProfile

# Create your models here.
class Category(models.Model):
    PART_TIME = 'PT'
    FULL_TIME = 'FT'
    CATEGORY_CHOICES = [
        (PART_TIME, 'Part-time'),
        (FULL_TIME, 'Full-time'),
    ]
    name = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    def __str__(self):
        # built-in Django method
        return self.get_name_display()
class Job(models.Model):
    title = models.CharField(max_length=100) # mandatory
    description = models.TextField() # mandatory
    # each Job instance is associated with one Category instance, but each Category instance can be associated with many Job instances.
    job_type = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='jobs') # mandatory
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # optional
    city = models.CharField(max_length=100) # mandatory
    country = models.CharField(max_length=100) # mandatory
    company = models.CharField(max_length=100) # mandatory
    created_at = models.DateTimeField(auto_now_add=True) # mandatory  
    employer = models.ForeignKey(EmployerUser, on_delete=models.CASCADE, related_name='jobs') # mandatory
    def __str__(self):
        return self.title

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    def __str__(self):
        return self.user.username
    
class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    job = models.ForeignKey(Job, on_delete=models.PROTECT)
    profile = models.ForeignKey(ApplicantProfile, on_delete=models.PROTECT)
    def __str__(self):
        return self.user.username
