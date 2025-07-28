from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobSeekerProfileForm, EducationForm, CertificationForm, JobExperienceForm
from .models import JobSeekerProfile, Skill, JobApplication
from employeer.models import Job
from django.conf import settings 
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view
from .serializers import JobSeekerProfileSerializer, SkillSerializer, JobSeekerProfileCreateSerializer, JobSerializer
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib import messages


@login_required
def jobseeker_profile_page(request):
    if hasattr(request.user, 'job_seeker_profile'):
        return redirect('job_seeker_dashboard')  # Prevent duplicate profile

    return render(request, 'job_seeker/create_js_profile.html')

class SkillListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class JobSeekerProfileCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = JobSeekerProfileCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)
        if serializer.is_valid():
            profile = serializer.save()
            return Response({'message': 'Profile created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        profile = get_object_or_404(JobSeekerProfile, user=request.user)
        data = {
            'js_name': profile.name,
            'js_email': profile.email,
            'js_skills': profile.skills,
        }
        return JsonResponse(data)

@login_required
def create_job_seeker_profile(request):
    user = request.user
    # Redirect if profile already exists
    if hasattr(user, 'job_seeker_profile'):
        return redirect('user:profile')  # ✅ Fix applied here

    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('job_seeker_dashboard')

    return render(request, 'job_seeker/create_js_profile.html')

@login_required
def job_seeker_dashboard(request):
    profile = get_object_or_404(JobSeekerProfile, user=request.user)
    return render(request, 'job_seeker/dashboard.html', {'profile': profile})

class JobSeekerProfileDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = JobSeekerProfile.objects.get(user=request.user)
        except JobSeekerProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
        
        serializer = JobSeekerProfileSerializer(profile)
        return Response(serializer.data)

@login_required
def employer_profile_api(request):
    profile = get_object_or_404(JobSeekerProfile, user=request.user)
    data = {
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'email': profile.email,
        'about': profile.about,
    }
    return JsonResponse(data)

class JobSearchAPIView(APIView):
    def get(self, request):
        name = request.GET.get('name', '').strip()
        job_type = request.GET.get('type', '').strip()
        skills_param = request.GET.get('skills', '').strip()

        queryset = Job.objects.all()

        if name:
            queryset = queryset.filter(job_title__icontains=name)

        if job_type:
            queryset = queryset.filter(type__iexact=job_type)

        if skills_param:
            skill_names = [s.strip() for s in skills_param.split(',') if s.strip()]
            if skill_names:
                queryset = queryset.filter(skills__name__in=skill_names).distinct()

        job_list = []
        for job in queryset:
            job_data = JobSerializer(job).data
            job_data['has_applied'] = job.applications.filter(applicant=request.user).exists()
            job_list.append(job_data)

        return Response(job_list)

@login_required
def job_search_page(request):
    return render(request, 'job_seeker/job_search.html')

@api_view(['POST'])
@login_required
def apply_job(request):
    if request.method == 'POST':
        job_id = request.data.get('job_id')

        if not job_id:
            return Response({'detail': 'Missing job_id'}, status=400)

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'detail': 'Job not found'}, status=404)

        if JobApplication.objects.filter(job=job, applicant=request.user).exists():
            return Response({'detail': 'Already applied'}, status=400)

        JobApplication.objects.create(job=job, applicant=request.user)
        return Response({'message': 'Application successful'}, status=201)

@login_required
def my_applications_page(request):
    applications = JobApplication.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'job_seeker/my_applications.html', {'applications': applications})

@login_required
def view_job_seeker_profile(request):
    profile = get_object_or_404(JobSeekerProfile, user=request.user)
    return render(request, 'job_seeker/profile_detail.html', {'profile': profile})

@login_required
def delete_job_seeker_account(request):
    if request.method == 'POST':
        user = request.user
        try:
            job_seeker_profile = get_object_or_404(JobSeekerProfile, user=user)
            job_seeker_profile.delete()  # Delete profile
            user.delete()  # Delete the user account
            logout(request)
            messages.success(request, "Your job seeker account and all data have been deleted.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Error deleting account: {e}")
            return redirect('job_seeker_profile')