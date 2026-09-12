from django.contrib import admin
from .models import ContactMessage



@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'message', 'is_read']
    list_filter = ['is_read']
    list_editable = ['is_read']
    search_fields = ['id', 'name', 'email', 'subject', 'message']
    list_display_links = ['id', 'message']
    ordering = ['-created_at']