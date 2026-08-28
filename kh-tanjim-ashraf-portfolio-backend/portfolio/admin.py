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
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(ContactMessage)