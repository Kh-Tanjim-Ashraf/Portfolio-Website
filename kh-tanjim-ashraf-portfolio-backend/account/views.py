from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserLoginSerializer, OwnerInfoSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from utils.jwt_token_generator import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated


class Login(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)

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



class OwnerInfo(APIView):
    # API/View-level permission; Compels the user to send access token through the `Headers` of the reaquest
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = OwnerInfoSerializer(request.user)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)