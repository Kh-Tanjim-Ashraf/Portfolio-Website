from rest_framework import serializers
from django.contrib.auth import get_user_model



User = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'password']



class OwnerInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']