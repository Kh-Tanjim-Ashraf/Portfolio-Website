from django.contrib import admin
from .models import Skill, Project, Experience, Education, ContactMessage


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'display_order', 'is_featured']
    list_filter = ['category', 'is_featured']
    ordering = ['display_order', '-proficiency']

admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(ContactMessage)