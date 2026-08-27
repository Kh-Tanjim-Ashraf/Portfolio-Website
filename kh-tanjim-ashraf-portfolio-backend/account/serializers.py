from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import Profile


User = get_user_model()


# Authentication
class UserLoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'password']



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, attrs):
        old_password = attrs['old_password']
        new_password = attrs['new_password']
        user = self.context['user']

        # Check if the given old_password matches the associted password stored in the DB
        if not check_password(attrs['old_password'], user.password):
            raise serializers.ValidationError({"old_password": "Invalid old password!"})

        # Prevent settings the same password
        if old_password == new_password:
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the old password."})

        return super().validate(attrs)



# Profile
class OwnerInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'full_name',
            'headline',
            'bio',
            'phone',
            'location',
            'avatar',
            'resume',
            'github_url',
            'linkedin_url',
            'x_url',
            'website_url',
            'years_of_experience',
            'is_available_for_hire'
        ]

    # Note: Since this method only sanitize the 'avatar' attribute, unlike the 'validate' method, naming the parameter 'value' makes more sense than 'attrs' 
    def validate_avatar(self, value):
        valid_extensions = ['png','jpg','jpeg','webp']
        ext = value.name.split('.')[-1].lower()

        # File extension check
        if ext not in valid_extensions:
            raise serializers.ValidationError("Only PNG, JPG, JPEG & WEBP images are allowed.")

        # File size check (5MB limit)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Avatar file size cannot exceed 5MB.")

        return value

    def validate_resume(self, value):
        valid_extensions = ['pdf']
        ext = value.name.split(".")[-1].lower()

        # File extension check
        if ext not in valid_extensions:
            raise serializers.ValidationError("Resume must be in PDF format.")

        # File size check (10MB limit)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Resume file size cannot exceed 10MB.")

        return value