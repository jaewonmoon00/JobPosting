
from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_applicant_profile, name='create_profile'),
    path('<int:profile_id>/', view_applicant_profile, name='view_profile'),
    path('<int:profile_id>/edit/', edit_applicant_profile, name='edit_profile'),
    path('', profiles_main, name='profiles_main'),
    path('<int:profile_id>/delete', delete_applicant_profile, name='delete_profile')
]