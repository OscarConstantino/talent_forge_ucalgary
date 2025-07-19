# employer/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import EmployerProfileForm, JobForm
from .models import EmployerProfile, Job
from job_seeker.models import Skill

@login_required
def create_employer_profile(request):
    user = request.user
    # Redirect if profile already exists
    if hasattr(user, 'employerprofile'):
        
        return redirect('user:profile')  # ✅ Fix applied here

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm()
    
    return render(request, 'employer/create_profile.html', {'profile_form': form})

@login_required
def employer_dashboard(request):
    profile = get_object_or_404(EmployerProfile, user=request.user)
    return render(request, 'employer/dashboard.html', {'profile': profile})

@login_required
def employer_profile_api(request):
    profile = get_object_or_404(EmployerProfile, user=request.user)
    data = {
        'company_name': profile.name,
        'email': profile.email,
        'industry': profile.industry,
    }
    return JsonResponse(data)

@login_required
def create_job(request):
    employer_profile = get_object_or_404(EmployerProfile, user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer_profile
            job.save()
            skill_names = request.POST.get('skills_text', '').split(',')
            for name in filter(None, map(str.strip, skill_names)):
                skill, _ = Skill.objects.get_or_create(name=name)
                job.skills.add(skill)

            return redirect('job_list')  # success redirect
    else:
        form = JobForm()

    skills = Skill.objects.values('id', 'name')  # Send to React
    return render(request, 'employer/create_job.html', {
        'form': form,
        'all_skills': list(skills)
    })

@login_required
def job_list(request):
    employer_profile = get_object_or_404(EmployerProfile, user=request.user)
    # Filter jobs to show only those belonging to this specific employer_profile
    jobs = Job.objects.filter(employer=employer_profile).prefetch_related('skills')

    return render(request, 'employer/job_list.html', {'jobs': jobs})