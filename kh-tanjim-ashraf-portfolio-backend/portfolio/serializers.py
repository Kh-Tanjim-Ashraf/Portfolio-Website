from rest_framework import serializers
from .models import Skill, Experience


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['name','category','proficiency','icon','display_order','is_featured']



class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = ['company','role','employment_type','location','start_date','end_date','is_current','description','company_url','display_order']