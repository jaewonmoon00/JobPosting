from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Job, Application
from django.urls import reverse_lazy # returns a URL as a string
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponseForbidden
from user_management.models import EmployerUser, ApplicantUser
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.models import ApplicantProfile

# Create your views here.
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostListView(ListView):
    model = Job
    template_name = 'jobposting/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    def get_queryset(self):
        # Access the request object with self.request
        search_term = self.request.GET.get('search_term', '')
        city = self.request.GET.get('city', None)
        country = self.request.GET.get('country', '')
        salary_max = self.request.GET.get('salary_max', '')
        salary_min = self.request.GET.get('salary_min', '')
        print(search_term, city, country, salary_max, salary_min)
        # If none of the search parameters are present, return all jobs
        if not any([search_term, city, country, salary_max, salary_min]):
            return Job.objects.all()

        # Convert salary_max and salary_min to float if they are not empty strings
        if salary_max != '':
            salary_max = float(salary_max)
        if salary_min != '':
            salary_min = float(salary_min)

        # Filter the jobs based on the search term and country
        jobs = Job.objects.filter(Q(title__icontains=search_term) | Q(description__icontains=search_term), country__icontains=country)

        # If city is not an empty string, add a filter for city
        if city != '':
            jobs = jobs.filter(city__icontains=city)

        # If salary_max is not an empty string, add a filter for salary_max
        if salary_max != '':
            jobs = jobs.filter(salary__lte=salary_max)

        # If salary_min is not an empty string, add a filter for salary_min
        if salary_min != '':
            jobs = jobs.filter(salary__gte=salary_min)

        return jobs

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = 'jobposting/post_detail.html'
    context_object_name = 'post'
    login_url = reverse_lazy('user_management:log-in')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        try:
            user = EmployerUser.objects.get(username=self.request.user.username)
            context['user_type'] = 'employer'
        except EmployerUser.DoesNotExist:
            try:
                user = ApplicantUser.objects.get(username=self.request.user.username)
                context['user_type'] = 'applicant'
            except ApplicantUser.DoesNotExist:
                user = User.objects.get(username=self.request.user.username)
                context['user_type'] = 'admin'
        print(context['user_type'])
        return context
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Job
    template_name = 'jobposting/post_create.html'
    fields = ('title', 'description', 'job_type', 'salary', 'city', 'country', 'company')
    success_url = reverse_lazy('posts:post_list')
    login_url = reverse_lazy('user_management:log-in')
    def dispatch(self, request, *args, **kwargs):
        # Ensure the user is authenticated first
        if not request.user.is_authenticated:
            login_url = reverse_lazy('user_management:log-in')
            redirect_url = f"{login_url}?next={request.path}"
            return redirect(redirect_url)
            # return HttpResponseForbidden()
        try:        
            if isinstance(EmployerUser.objects.get(username=request.user.username), EmployerUser):
                return super().dispatch(request, *args, **kwargs)
            else: return HttpResponseForbidden()

        except EmployerUser.DoesNotExist:
            # case where the user is not an employer
            return HttpResponseForbidden()
    def form_valid(self, form):
        employer_user = EmployerUser.objects.get(username=self.request.user.username)
        print(type(employer_user))
        form.instance.employer = employer_user
        return super().form_valid(form)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'jobposting/post_delete.html'
    success_url = reverse_lazy('posts:post_list')
    login_url = reverse_lazy('user_management:log-in')
    def dispatch(self, request, *args, **kwargs):
        # TODO: delete button will not be displayed to applicants, but it's better to prevent applicant from
        # TODO: accessing the delete view (using try catch)
        employer_user = EmployerUser.objects.get(username=self.request.user.username)
        job = Job.objects.get(pk=self.kwargs['pk']).employer
        # compare
        if employer_user == job:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    template_name = 'jobposting/post_update.html'
    fields = ('title', 'description', 'job_type', 'salary', 'city', 'country', 'company')
    success_url = reverse_lazy('posts:post_list')
    login_url = reverse_lazy('user_management:log-in')
    def dispatch(self, request, *args, **kwargs):
        # TODO: update button will not be displayed to applicants, but it's better to prevent applicant from
        # TODO: accessing the update view (using try catch)
        employer_user = EmployerUser.objects.get(username=self.request.user.username)
        job = Job.objects.get(pk=self.kwargs['pk']).employer
        # compare
        if employer_user == job:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

class PostApplyView(LoginRequiredMixin, View):
    template_name = 'jobposting/post_apply.html'
    login_url = reverse_lazy('user_management:log-in')
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Job, pk=kwargs['pk'])  # Get the post object
        # Fetch the profiles of the current user
        profiles = ApplicantProfile.objects.filter(user=request.user)
        # If no profiles exist, redirect the user to the profile creation page
        if not profiles.exists():
            return redirect('profiles:create_profile')  # replace 'profile_create' with the actual name of your profile creation view
        # Pass the profiles to the template
        context = {'profiles': profiles, 'post': post}
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Job, pk=kwargs['pk'])
        profile_id = request.POST.get('profile_id')
        profile = get_object_or_404(ApplicantProfile, pk=profile_id)
        # create Application model

        #if (request.POST.get('abilities_skills') == "aaaaa"):

        profile = ApplicantProfile.objects.create(user=profile.user, applicant_profile_name=profile.applicant_profile_name, past_work_experience=request.POST.get('past_work_experience'), 
                                                  abilities_skills=request.POST.get('abilities_skills'), education=request.POST.get('education'),
                                                  achievement_honors=request.POST.get('achievement_honors'), tell_the_employer=request.POST.get('tell_the_employer'), is_copy=True)

        application = Application.objects.create(user=profile.user, job=post, profile=profile)
        application.save()
        return redirect('posts:post_list')
    # TODO: prevent applicant from applying to the same job twice
    # TODO: limit this view to only applicants

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# class ApplicationListView(LoginRequiredMixin, ListView):
#     # this view is available to only employers
#     # display only applications to the posts that belong to currently logged in employer
#     model = Application
#     template_name = 'jobposting/application_list.html'
#     context_object_name = 'applications'
#     login_url = reverse_lazy('user_management:log-in')
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             EmployerUser.objects.get(username=request.user.username)
#             return super().dispatch(request, *args, **kwargs)
#         except EmployerUser.DoesNotExist:
#             return HttpResponseForbidden()
#     def get_queryset(self):
#         #TODO: check if below works
#         employer_user = EmployerUser.objects.get(username=self.request.user.username)
#         return Application.objects.filter(job__employer=employer_user)
    