from rest_framework import serializers
from .models import ContactMessage



class ContactsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactMessage
        fields = ['id','name','email','subject','message','is_read','created_at','updated_at']
        read_only_fields = ['id','is_read']