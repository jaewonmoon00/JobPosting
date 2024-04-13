from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from jobposting.models import *
from .forms import *
from django.contrib.auth.models import User
from profiles.models import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

@login_required
def employer_main(request):
    # Set to false for now
    try:
        employer_user = EmployerUser.objects.get(username=request.user.username)
        employer_verified = employer_user.documents_authenticated
        verification_in_progress = employer_user.verification_in_progress

        context = {
            'employer_verified': employer_verified,
            'verification_in_progress': verification_in_progress
        }
        # Add any necessary logic here
        return render(request, 'employer_main.html', context)
    except EmployerUser.DoesNotExist:
        # not authorized. you are logged in as an applicant
        return HttpResponseForbidden()

@login_required
def employer_verify(request):
    context = {}

    # Create object of form
    form = EmployerVerificationForm(request.POST or None, request.FILES or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        employer_verification = form.save(commit=False)
        employer_verification.employer = Employer.objects.get(user=request.user) 
        employer_verification.save()
        user = EmployerUser.objects.get(username=request.user.username)
        user.verification_in_progress = True
        user.save()
        return redirect('employer:employer_main')

    context['form']= form
    return render(request, "employer_verify.html", context)

@login_required
def employer_verify_view(request):
    user = User.objects.get(username=request.user.username)
    employer = Employer.objects.get(user=user)
    employer_verification = EmployerVerification.objects.get(employer=employer)

    return render(request, 'employer_view_verification.html', {'employer_verification': employer_verification})

@login_required
def employer_verify_cancel(request):
    user = User.objects.get(username=request.user.username)
    employer = Employer.objects.get(user=user)
    employer_user = EmployerUser.objects.get(username=request.user.username)
    employer_user.verification_in_progress = False
    employer_user.save()
    employer_verification = EmployerVerification.objects.get(employer=employer)

    employer_verification.file1.delete(save=False)
    employer_verification.file2.delete(save=False)
    employer_verification.business_logo.delete(save=False)

    employer_verification.delete()

    return redirect('employer:employer_main')

@login_required
def employer_company(request):
    # Assuming the user is authenticated and has an associated employer
    employer = Employer.objects.get(user=request.user)
    employer_verification = EmployerVerification.objects.get(employer=employer)
    return render(request, 'employer_company.html', {'employer': employer, 'employer_verification': employer_verification})

@login_required
def employer_jobs(request):
    # Assuming the user is authenticated and has an associated employer
    employer = employer = Employer.objects.get(user=request.user)
    jobs = Job.objects.filter(employer=request.user)
    return render(request, 'employer_jobs.html', {'jobs': jobs, 'employer': employer})

def employer_job_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_details.html', {'job': job})

def employer_job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applicants = Application.objects.filter(job=job)
    return render(request, 'job_applicants.html', {'job': job, 'applicants': applicants})

def employer_job_applicant_profile(request, job_id, applicant_id):
    job = get_object_or_404(Job, id=job_id)
    applicant = get_object_or_404(Application, id=applicant_id)

    applicant_profile = applicant.profile

    # try:
    #     applicant_profile = ApplicantProfile.objects.filter(user=applicant.user).first()
    #     if not applicant_profile:
    #         raise Http404("No ApplicantProfile found.")
    # except ApplicantProfile.DoesNotExist:
    #     raise Http404("No ApplicantProfile found.")
    return render(request, 'job_applicant_profile.html', {'job_id': job_id, 'applicant_id': applicant_id, 'applicant_profile': applicant_profile})


def employer_job_applicant_interest(request, job_id, applicant_id):
    applicant = get_object_or_404(Application, id=applicant_id)
    user = request.user

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    to = [user.username, applicant.user.username]
    fromEmail = "privacyjobboard@gmail.com" 
    password = "euoq nrjx lmdc moks"
    email_message = MIMEMultipart('alternative')
    email_message["Subject"] = "JOB APPLICATION INTEREST CONFIRMED EMAIL EXCHANGE"
    email_message["From"] = fromEmail
    email_message["To"] = ", ".join(to)

    html = """\
    <html>
    <body>
        <p>The emails of both parties are: {}</p>
    </body>
    </html>
    """.format(to)

    email_message.attach(MIMEText(html, "html"))
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(fromEmail, password)
        server.sendmail(fromEmail, to, email_message.as_string())

    return redirect('/employer')

# Only admins should have access
def employer_verification_confirm(request, id):
    user = EmployerUser.objects.get(username=id)
    employer = Employer.objects.get(user=user)
    employer_verification = EmployerVerification.objects.get(employer=employer)

    employer_verification.file1.delete(save=False)
    employer_verification.file2.delete(save=False)

    user.documents_authenticated = True
    user.verification_in_progress = False
    user.public_key = employer_verification.public_key
    user.save()

    return redirect('/')
    
# Only admins should have access
def employer_verification_deny(request, id):
    user = User.objects.get(username=id)
    employer = Employer.objects.get(user=user)
    employer_user = EmployerUser.objects.get(username=request.user.username)
    employer_user.verification_in_progress = False
    employer_user.save()
    employer_verification = EmployerVerification.objects.get(employer=employer)

    employer_verification.file1.delete(save=False)
    employer_verification.file2.delete(save=False)
    employer_verification.business_logo.delete(save=False)

    employer_verification.delete()

    return redirect('/')