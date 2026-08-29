from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserLoginSerializer, OwnerInfoSerializer, ChangePasswordSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from utils.jwt_token_generator import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Profile as ProfileModel
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class Login(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)

            # Mitigate AttributeError: NoneType' object has no attribute 'id' while accessing authenticated/anon user
            if not user:
                data = {"error": "Invalid credentials."}
                return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
            
            tokens = get_tokens_for_user(user)
        
            data = {
                'access': tokens.get('access_token'),
                'refresh': tokens.get('refresh_token'),
                'user': {
                    'id': user.id,
                    'username': user.username, 
                    'email': user.email
                }
            }

            return Response(data=data, status=status.HTTP_200_OK)



class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        serializer = ChangePasswordSerializer(data=request.data, context={'user': user})

        if serializer.is_valid(raise_exception=True):
            # Change the old password; Beaware to make the password hashed
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            
            data = {"message": "Passowrd has changed successfully."}
            return Response(data=data, status=status.HTTP_200_OK)



class OwnerInfo(APIView):

    # API/View-level permission; Compels the user to send access token through the `Headers` of the reaquest
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = OwnerInfoSerializer(request.user)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class Profile(APIView):

    # Apply permissions dynamically based on the request types: GET->Public; PATCH->Protected
    def get_permissions(self):
        # Evaluate the request type & assign permission class(es) accordingly
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]

        if self.request.method == "PATCH":
            self.permission_classes = [IsAuthenticated]

        # Instantiate & returns the list of permission class(es) on the fly by adding the `()` 
        return [permission() for permission in self.permission_classes]

    def get(self, request):
        # Public API, thus returns my single profile record to any `GET` request
        profile = ProfileModel.objects.first()
        serializer = ProfileSerializer(instance=profile)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        # Retrieve the profile belonging to the authenticated user
        try:
            userProfile = ProfileModel.objects.get(user=request.user)
        except ProfileModel.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(instance=userProfile, data=request.data, partial=True)   # TODO: Require to pass the request through context to the serializer in order to help it building absolute URLs; Inspect this

        if serializer.is_valid(raise_exception=True):

            # Clean up old files from storage before saving new ones; TODO: Require further inspection
            if 'avatar' in request.FILES and userProfile.avatar:
                userProfile.avatar.delete(save=False)

            if 'resume' in request.FILES and userProfile.resume:
                userProfile.resume.delete(save=False)
            
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)



# Blacklist specific refresh token
class Logout(APIView):

    def post(self, request):
        try:
            # Retrieve the refresh token
            refresh_token = request.data.get("refresh")

            # Check if any refresh_token is passed in the request body
            if not refresh_token:
                return Response(data={"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Instantiating the `RefreshToken` dynamically checks the validity of the token
            token = RefreshToken(token=refresh_token)

            # Blacklist the specific token
            token.blacklist()

            return Response(data={"message":"Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            # Handle invalid, expired or already blacklisted tokens
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)