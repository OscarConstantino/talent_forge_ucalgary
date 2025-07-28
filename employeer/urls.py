from django.urls import path
from . import views

urlpatterns = [
    path('create_employer_profile/', views.create_employer_profile, name='create_employer_profile'),
    path('employer_dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('api/employer/profile/', views.employer_profile_api, name='employer-profile-api'),
    path('create_job/', views.create_job, name='create_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/applications/', views.job_applications, name='job_applications'),
    path('jobs/application/<int:application_id>/update_status/', views.update_application_status, name='update_application_status'),
    path('employer/profile/', views.view_employer_profile, name='employer_profile'),
    path('delete/', views.delete_employer_account, name='delete_employer_account'),
]