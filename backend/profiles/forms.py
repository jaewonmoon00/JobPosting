from django import forms
from .models import ApplicantProfile
# from .encryption import encrypt_data

class ApplicantForm(forms.ModelForm):
    encrypted_fields = ["past_work_experience", "abilities_skills", "education", "achievement_honors", "tell_the_employer"]

    class Meta:
        model = ApplicantProfile
        fields = ["applicant_profile_name", "past_work_experience", "abilities_skills", "education", "achievement_honors", "tell_the_employer"]

    # def save(self, commit=True):
    #     instance = super(ApplicantForm, self).save(commit=False)
    #     for field_name in self.encrypted_fields:
    #         if field_name in self.cleaned_data:
    #             # Encrypt the field before saving
    #             encrypted_value = encrypt_data(self.cleaned_data[field_name])
    #             setattr(instance, field_name, encrypted_value)
    #     if commit:
    #         instance.save()
    #     return instance
