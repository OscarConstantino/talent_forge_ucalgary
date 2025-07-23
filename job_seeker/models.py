from django.db import models
from user.models import CustomUser
from django.conf import settings

# Create your models here.
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='job_seeker_profile')
    first_name = models.CharField(max_length=150)  # align with Django's default User model
    last_name = models.CharField(max_length=150)
    location = models.CharField(max_length=255)  # can be city, region, etc.
    role = models.CharField(max_length=100)  # title like 'Software Engineer', 'Data Analyst', etc.
    picture = models.ImageField(upload_to='job_seeker_profile/', blank=True)
    phone_number = models.CharField(max_length=20)  # country code + local (e.g., +1-234-567-8901)
    industry = models.CharField(max_length=100)  # e.g., 'Finance', 'IT', etc.
    about = models.TextField(blank=True)  # ✅ better than URLField if this is a bio or description
    resume = models.ImageField(upload_to='job_seeker_profile/resume/', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

    skills = models.ManyToManyField('Skill', through='JobSeekerSkill', related_name='job_seekers')

class Education(models.Model):
    job_seeker = models.ForeignKey(
        'JobSeekerProfile',
        on_delete=models.CASCADE,
        related_name='educations'
    )
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

class JobExperience(models.Model):
    job_seeker = models.ForeignKey(
        'JobSeekerProfile',
        on_delete=models.CASCADE,
        related_name='job_experiences'
    )
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    responsibilities = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} at {self.company_name}"


class Certification(models.Model):
    job_seeker = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name='certifications'
    )
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.issuer}"

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class JobSeekerSkill(models.Model):  # if using through model
    job_seeker = models.ForeignKey('JobSeekerProfile', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    proficiency = models.CharField(
        max_length=50,
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
            ('Expert', 'Expert'),
        ]
    )

    class Meta:
        unique_together = ('job_seeker', 'skill')

    def __str__(self):
        return f"{self.job_seeker} - {self.skill} ({self.proficiency})"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'), # Keep 'submitted' as the initial default
        ('under_review', 'Under Review'),
        ('interview', 'Interview'),
        ('final_round', 'Final Round'), # New option
        ('selected', 'Selected'),       # New option
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey('employeer.Job', on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')

    class Meta:
        unique_together = ('job', 'applicant')  # prevents duplicate applications

    def __str__(self):
        return f"{self.applicant.email} applied to {self.job.job_title}"