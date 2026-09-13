from rest_framework import serializers
from .models import ContactMessage



class ContactsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactMessage
        fields = ['id','name','email','subject','message','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']



class ContactsDetailSerializer(ContactsSerializer):
    '''
    Identical but handles administrative API endpoints
    '''
    class Meta:
        model = ContactsSerializer.Meta.model
        fields = ContactsSerializer.Meta.fields + ['is_read']