from django.shortcuts import render
from .models import Skill, Experience, Education as EducationModel, Project
from rest_framework.views import APIView
from .serializers import SkillSerializer, ExperienceSerializer, EducationSerializer, ProjectSerializer
from rest_framework.response import Response
from rest_framework import status
from .filters import SkillFilter
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.custom_pagination import CustomPagination



# Skill
class Skills(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]

        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        
        return [permission() for permission in self.permission_classes]

    def get(self, request):
        queryset = Skill.objects.all()

        filterset = SkillFilter(data=request.query_params, queryset=queryset)

        serializer = SkillSerializer(instance=filterset.qs, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
            serializer = SkillSerializer(data=request.data)
    
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)



class SkillDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        queryset = get_object_or_404(Skill, pk=id)

        serializer = SkillSerializer(instance=queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        queryset = get_object_or_404(Skill, pk=id)

        serializer = SkillSerializer(instance=queryset, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        queryset = get_object_or_404(Skill, pk=id)

        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



# Experience
class Experiences(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]

        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def get(self, request):
        queryset = Experience.objects.all()

        serializer = ExperienceSerializer(instance=queryset, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
            serializer = ExperienceSerializer(data=request.data)
    
            if serializer.is_valid(raise_exception=True):
                serializer.save()
    
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)



class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        queryset = get_object_or_404(Experience, pk=id)

        serializer = ExperienceSerializer(instance=queryset)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        queryset = get_object_or_404(Experience, pk=id)

        serializer = ExperienceSerializer(instance=queryset, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        queryset = get_object_or_404(Experience, pk=id)

        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



# Education
class Education(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]

        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        
        return [permission() for permission in self.permission_classes]

    def get(self, request):
        queryset = EducationModel.objects.all()

        serializer = EducationSerializer(instance=queryset, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EducationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)



class EducationDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        queryset = get_object_or_404(EducationModel, pk=id)

        serializer = EducationSerializer(instance=queryset)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        queryset = get_object_or_404(EducationModel, pk=id)

        serializer = EducationSerializer(instance=queryset, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        queryset = get_object_or_404(EducationModel, pk=id)

        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



# Project
class Projects(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]

        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def get(self, request):
        # Mandatory to use `order_by` while using pagination; To mitigate the `N+1 Query` issue, the `prefetch_related()` ORM method is defined
        queryset = Project.objects.prefetch_related('skill').order_by('id')

        paginator = CustomPagination(page_size=9)

        paginated_queryset = paginator.paginate_queryset(queryset=queryset, request=request, view=self)

        serializer = ProjectSerializer(paginated_queryset, many=True)

        response = paginator.get_paginated_response(serializer.data)

        response.status_code = status.HTTP_206_PARTIAL_CONTENT

        return response

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)



class ProjectDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        queryset = get_object_or_404(Project, slug=slug)

        serializer = ProjectSerializer(instance=queryset)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        queryset = get_object_or_404(Project, slug=slug)
        
        serializer = ProjectSerializer(instance=queryset, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        queryset = get_object_or_404(Project, slug=slug)

        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)