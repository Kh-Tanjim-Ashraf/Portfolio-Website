from django.contrib import admin
from .models import Skill, Project, Experience, Education, ContactMessage


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'proficiency', 'display_order', 'is_featured']
    list_filter = ['category', 'proficiency', 'is_featured']
    ordering = ['display_order', '-proficiency']
    # Search accorss relationships (foreign keys) using `__`; Ttechnique is also allowed to be used in any other class attributes
    search_fields = ['id', 'name', 'category', 'proficiency', 'display_order']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_skills', 'summary', 'category', 'live_url', 'is_featured', 'completed_date', 'display_order']

    # Display `skill` as string, since it's a M2M field
    def get_skills(self, obj):
        return ', '.join([tag.name for tag in obj.skill.all()])

    get_skills.short_description = 'Skill'

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'role', 'employment_type', 'start_date', 'end_date', 'is_current', 'display_order']
    list_filter = ['employment_type', 'is_current', 'start_date', 'end_date']
    search_fields = ['company', 'role', 'employment_type', 'location', 'start_date', 'end_date', 'description', 'company_url', 'display_order']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['id', 'instituition', 'degree', 'field_of_study', 'start_year', 'end_year', 'grade', 'description']
    list_filter = ['start_year', 'end_year']
    search_fields = ['instituition', 'degree', 'field_of_study', 'start_year', 'end_year', 'grade', 'description']

admin.site.register(ContactMessage)