from django.db import models
from django.contrib.auth.models import User


class ApplicantProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)
    applicant_profile_name = models.CharField(max_length=255)
    past_work_experience = models.TextField()
    abilities_skills = models.TextField()
    education = models.TextField()
    achievement_honors = models.TextField()
    tell_the_employer = models.TextField()
    is_copy = models.BooleanField(default=False)

    def __str__(self):
        #return self.applicant_profile_name
        return '{} - {}'.format(self.pk, self.applicant_profile_name)