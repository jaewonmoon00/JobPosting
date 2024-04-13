from django.urls import path
from .views import *

urlpatterns = [
    path('', employer_main, name='employer_main'),
    path('verify', employer_verify, name='employer_verify'),
    path('verify/view', employer_verify_view, name='employer_verify_view'),
    path('verify/cancel', employer_verify_cancel, name='employer_verify_cancel'),
    path('company', employer_company, name='employer_company'),
    path('jobs', employer_jobs, name='employer_jobs'),
    path('jobs/<int:job_id>', employer_job_details, name='employer_job_details'),
    path('jobs/<int:job_id>/applicants', employer_job_applicants, name='employer_job_applicants'),
    path('jobs/<int:job_id>/applicants/<int:applicant_id>', employer_job_applicant_profile, name='employer_job_applicant_profile'),
    path('jobs/<int:job_id>/applicants/<int:applicant_id>/interest', employer_job_applicant_interest, name='employer_job_applicant_interest'),


    path('verification/<str:id>/confirm', employer_verification_confirm, name='employer_verification_confirm'),
    path('verification/<str:id>/deny', employer_verification_deny, name='employer_verification_deny')

]