from django.shortcuts import render
from django.views import View

# Create your views here.
class PrivacyPolicyView(View):
    template_name = 'privacy_policy/privacy_policy.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)