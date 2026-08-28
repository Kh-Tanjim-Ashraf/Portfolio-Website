from django.shortcuts import render
from .models import Skill as SkillModel
from rest_framework.views import APIView
from .serializers import SkillSerializer
from rest_framework.response import Response
from rest_framework import status
from .filters import SkillFilter



class Skill(APIView):

    def get(self, request):
        queryset = SkillModel.objects.all()

        filterset = SkillFilter(data=request.query_params, queryset=queryset)

        serializer = SkillSerializer(instance=filterset.qs, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)