from rest_framework import serializers
from .models import Skill, Experience, Education, Project


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['name','category','proficiency','icon','display_order','is_featured']



class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = ['company','role','employment_type','location','start_date','end_date','is_current','description','company_url','display_order']



class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = ['instituition','degree','field_of_study','start_year','end_year','grade','description']



class ProjectsSerializer(serializers.ModelSerializer):

    # Note: Since the project list requires only skill names, instead of the entire object of skillset, thus a `StringRelatedField` is more appropriate; It displays the `__str__` method of the model; 
    # Tips: As it is used for the public API, it will reduce the bandwidth.
    skill = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['title', 'slug', 'skill', 'summary', 'description', 'cover_image', 'category', 'live_url', 'github_url', 'is_featured', 'completed_date', 'display_order']