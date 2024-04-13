from django import forms
from .models import *

class EmployerVerificationForm(forms.ModelForm):

    class Meta:
        model = EmployerVerification
        fields = ["company_name", "business_address", "company_description", "business_contact_info", "business_logo", "file1", "file2", "public_key"]