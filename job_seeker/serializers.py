from rest_framework import serializers
from .models import (
    JobSeekerProfile, Education, Certification, Skill, JobSeekerSkill, JobExperience
)
from user.models import CustomUser
from employeer.models import Job, EmployerProfile


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ('job_seeker',)


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        exclude = ('job_seeker',)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']

class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        exclude = ('job_seeker',)

class JobSeekerSkillSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='skill.name')  # gets skill.name via foreign key

    class Meta:
        model = JobSeekerSkill
        fields = ['name', 'proficiency']

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    skills = JobSeekerSkillSerializer(source='jobseekerskill_set', many=True, read_only=True)
    job_experiences = JobExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = JobSeekerProfile
        exclude = ('user',)

class JobSeekerProfileCreateSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True)
    certifications = CertificationSerializer(many=True, required=False)
    skills = serializers.ListField(child=serializers.CharField())
    job_experiences = JobExperienceSerializer(many=True)

    class Meta:
        model = JobSeekerProfile
        exclude = ('user',)

    def create(self, validated_data):
        educations_data = validated_data.pop('educations', [])
        certifications_data = validated_data.pop('certifications', None) or []
        job_experiences_data = validated_data.pop('job_experiences', [])
        skills_data = validated_data.pop('skills', [])
        user = self.context['request'].user

        profile = JobSeekerProfile.objects.create(user=user, **validated_data)

        # Handle skills
        for name in skills_data:
            skill, _ = Skill.objects.get_or_create(name=name)
            JobSeekerSkill.objects.get_or_create(
                job_seeker=profile,
                skill=skill,
                defaults={'proficiency': 'Beginner'}  # Or adjust dynamically
            )

        # Handle educations
        for edu_data in educations_data:
            Education.objects.create(job_seeker=profile, **edu_data)

        # ✅ Handle certifications only if present
        for cert_data in certifications_data:
            Certification.objects.create(job_seeker=profile, **cert_data)

        return profile

class JobSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source='employer.name', read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'job_title', 'description', 'location', 'employer_name','work_mode']
