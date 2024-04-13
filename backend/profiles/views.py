from .forms import ApplicantForm
from .models import ApplicantProfile

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
 
@login_required
def create_applicant_profile(request):
    context ={}
 
    # create object of form
    form = ApplicantForm(request.POST or None, request.FILES or None)
     
    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        # After the profile is created, redirect to the URL specified by the 'next' parameter
        next_url = request.GET.get('next', 'profiles:profiles_main')
        return redirect(next_url)

    context['form']= form
    return render(request, "create_applicant_profile.html", context)

@login_required
def view_applicant_profile(request, profile_id):
    profile = ApplicantProfile.objects.get(pk=profile_id, user=request.user)

    return render(request, 'view_applicant_profile.html', {'profile': profile})

@login_required
def edit_applicant_profile(request, profile_id):
    profile = ApplicantProfile.objects.get(pk=profile_id, user=request.user)

    # create object of form
    form = ApplicantForm(request.POST or None, request.FILES or None, instance=profile)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        profile = form.save(commit=False)
        profile.save()
        
        return redirect('profiles:profiles_main')

    context ={}
    context['form']= form
    return render(request, 'edit_applicant_profile.html', context)

@login_required
def delete_applicant_profile(request, profile_id):
    profile = ApplicantProfile.objects.get(pk=profile_id, user=request.user)
    profile.delete()
    
    return redirect('profiles:profiles_main')

@login_required
def profiles_main(request):
    profiles = ApplicantProfile.objects.filter(user=request.user)

    return render(request, 'profiles_main.html', {'profiles': profiles})