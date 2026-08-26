from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


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