from django.urls import path
from .views import jobseeker_profile_page, JobSeekerProfileCreateAPIView, SkillListAPIView, JobSeekerProfileDetailAPIView, JobSearchAPIView
from . import views

urlpatterns = [
    # This serves the React page
    path('create_jobseeker_profile/', jobseeker_profile_page, name='create_jobseeker_profile'),
    path('job_seeker_dashboard/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
    # This is the API React POSTs to
    path('api/jobseeker/create/', JobSeekerProfileCreateAPIView.as_view(), name='api_create_jobseeker_profile'),
    path('api/skills/', SkillListAPIView.as_view(), name='skills-list'),
    path('api/jobseeker/profile/', JobSeekerProfileDetailAPIView.as_view(), name='jobseeker-profile'),
    path('api/jobs_search/', JobSearchAPIView.as_view(), name='job-search'),
    path('job_search_page/', views.job_search_page, name='job_search_page'),
]