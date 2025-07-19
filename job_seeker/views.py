from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobSeekerProfileForm, EducationForm, CertificationForm, JobExperienceForm
from .models import JobSeekerProfile, Skill
from employeer.models import Job
from rest_framework import generics
from django.conf import settings 
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import JobSeekerProfileSerializer, SkillSerializer, JobSeekerProfileCreateSerializer, JobSerializer
from django.db.models import Q


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

        serializer = JobSerializer(queryset, many=True)
        return Response(serializer.data)


@login_required
def job_search_page(request):
    return render(request, 'job_seeker/job_search.html')