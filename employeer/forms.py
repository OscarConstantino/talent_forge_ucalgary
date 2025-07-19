# employer/forms.py

from django import forms
from user.models import CustomUser
from .models import EmployerProfile, Job
from job_seeker.models import Skill
from django.contrib.auth.forms import UserCreationForm

class EmployerProfileForm(forms.ModelForm):

    terms_accepted = forms.BooleanField(
        required=True,
        label="I have read and agree to the Terms of Service", # This label will not be used if you manually render it in template
        error_messages={'required': 'You must accept the Terms of Service to register.'}
    )

    class Meta:
        model = EmployerProfile
        fields = ['name', 'email', 'logo', 'industry', 'number_employees', 'company_website', 'location', 'about']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        skills_text = forms.CharField(widget=forms.HiddenInput(), required=False)
        fields = ['job_title', 'description', 'location', 'type', 'work_mode']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'work_mode': forms.Select(),
            'skills': forms.SelectMultiple(attrs={'size': 6}),
        }
        labels = {
            'job_title': 'Job Title',
            'description': 'Job Description',
            'location': 'Location',
            'type': 'Job Type',
            'work_mode': 'Work Mode',
            'skills': 'Required Skills',
        }