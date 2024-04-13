from django import forms
from profiles.models import ApplicantProfile

class ApplyForm(forms.ModelForm):
    ApplicantProfile.objects.filter()
    profiles = forms.ModelChoiceField(queryset=ApplicantProfile.objects.all(), empty_label=None)
    def __init__(self, user, *args, **kwargs):
        self.fields['profiles'].queryset = ApplicantProfile.objects.filter()