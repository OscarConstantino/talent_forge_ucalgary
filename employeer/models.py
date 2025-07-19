from django.db import models
from user.models import CustomUser
from job_seeker.models import Skill

class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/',blank=True)  # Files will be stored in the 'company_logos' directory in your bucket
    email = models.EmailField(max_length=254)  # ✅ use EmailField for validation
    industry = models.CharField(max_length=100)
    company_website = models.URLField(blank=True)
    location = models.CharField(max_length=255)
    number_employees = models.IntegerField()
    about = models.TextField(blank=True)

    def __str__(self):
        return self.company_name

class Job(models.Model):
    class WorkMode(models.TextChoices):
        ON_SITE = 'on-site', 'On-site'
        REMOTE = 'remote', 'Remote'
        HYBRID = 'hybrid', 'Hybrid'

    employer = models.ForeignKey(
        'EmployerProfile',  # Reference the Employer model
        on_delete=models.CASCADE, # What happens when the referenced Employer is deleted
        related_name='jobs' # Allows you to do employer_instance.jobs.all()
    )

    job_title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=100)  # Example: "Full-time", "Part-time", "Internship"
    work_mode = models.CharField(
        max_length=10,
        choices=WorkMode.choices,
        default=WorkMode.ON_SITE
    )
    skills = models.ManyToManyField(Skill, related_name='jobs')

    def __str__(self):
        return self.job_title