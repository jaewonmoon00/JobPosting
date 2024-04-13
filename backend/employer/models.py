from django.db import models
from jobposting.models import Employer

def employer_file_upload_path(instance, filename):
    # Generate upload path based on employer's id
    return f'verification_files/{instance.employer.user.username}/{filename}'

class EmployerVerification(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    business_address = models.CharField(max_length=255)
    company_description = models.TextField()
    business_contact_info = models.CharField(max_length=255)
    business_logo = models.ImageField(upload_to=employer_file_upload_path)
    file1 = models.FileField(upload_to=employer_file_upload_path)
    file2 = models.FileField(upload_to=employer_file_upload_path)
    public_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employer.user.username}"