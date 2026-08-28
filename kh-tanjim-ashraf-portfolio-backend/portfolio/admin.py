from django.contrib import admin
from .models import Skill, Project, Experience, Education, ContactMessage


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'proficiency', 'display_order', 'is_featured']
    list_filter = ['category', 'proficiency', 'is_featured']
    ordering = ['display_order', '-proficiency']
    # Search accorss relationships (foreign keys) using `__`; Ttechnique is also allowed to be used in any other class attributes
    search_fields = ['id', 'name', 'category', 'proficiency', 'display_order']

admin.site.register(Project)

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