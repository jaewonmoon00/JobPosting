from django import forms
from .models import BaseUser, EmployerUser, ApplicantUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

EMPLOYER_STATUS = (("1", "Applicant"), ("2", "Employer"))
class SignUpForm(UserCreationForm):
    username = forms.EmailField(max_length=320, required=True)
    password1 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'data-toggle': 'password', 'id': 'password'}))
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'data-toggle': 'password', 'id': 'password'}))

    account_type = forms.ChoiceField(choices=EMPLOYER_STATUS)
    
    def save(self, commit=True):
        user_data = {
            'username': self.cleaned_data.get('username'),
            'password': self.cleaned_data.get('password1'),  # You might want to set password using user.set_password()
            # include other fields as necessary
        }
        account_type = self.cleaned_data.get('account_type')

        if account_type == "2":
            user = EmployerUser(**user_data)
        else:
            user = ApplicantUser(**user_data)

        if commit:
            # Use user.set_password(raw_password) here to properly handle password hashing
            user.set_password(self.cleaned_data.get('password1'))
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()

        return user

    class Meta:
        model = BaseUser
        fields = ['username', 'password1', 'password2', 'account_type']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=320, required=True)
    password = forms.PasswordInput()

    class Meta:
        model = BaseUser
        fields = ['username', 'password']

    