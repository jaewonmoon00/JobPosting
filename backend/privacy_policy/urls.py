from django.urls import path
from .views import PrivacyPolicyView

urlpatterns = [
    path('', PrivacyPolicyView.as_view(), name='privacy_policy'),
]