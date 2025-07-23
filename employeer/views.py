# employer/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import EmployerProfileForm, JobForm
from .models import EmployerProfile, Job
from job_seeker.models import Skill, JobApplication

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

@login_required
def job_applications(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    # Use the related_name 'applications' to get all applications for this job
    applications = job.applications.all().order_by('-applied_at') # Order by most recent

    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'employer/job_applications.html', context)

@login_required
def update_application_status(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(JobApplication, pk=application_id)

        # Basic permission check: Ensure the logged-in user (employer) has the right to modify this application.
        # This is a crucial step for security. You might want more sophisticated checks.
        # For example, check if the job associated with the application belongs to the current employer.
        # This example assumes request.user is an Employer type.
        if request.user.is_authenticated and request.user.user_type == '2': # '2' for Employer
            # Further check: Ensure the job associated with this application belongs to this employer
            # This requires the Job model to have a link to the employer (e.g., a ForeignKey to CustomUser)
            # Example (assuming Job has an 'employer' ForeignKey):
            # if application.job.employer != request.user:
            #     return redirect('permission_denied_page') # Or return HttpResponseForbidden

            new_status = request.POST.get('status')

            if new_status and new_status in [choice[0] for choice in JobApplication.STATUS_CHOICES]:
                application.status = new_status
                application.save()
                # Optionally add a success message
                # messages.success(request, f"Application status updated to {application.get_status_display()}")
            # else:
                # messages.error(request, "Invalid status provided.")
        # else:
            # messages.error(request, "You do not have permission to perform this action.")
            # return redirect('login') # Or wherever unauthenticated users should go

        # After updating, redirect back to the job applications page
        # Make sure 'job_applications' URL expects job_id
        return redirect('job_applications', job_id=application.job.id)