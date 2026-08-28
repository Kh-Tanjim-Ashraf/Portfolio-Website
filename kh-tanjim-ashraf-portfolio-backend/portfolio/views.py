from django.shortcuts import render
from .models import Skill as SkillModel
from rest_framework.views import APIView
from .serializers import SkillSerializer
from rest_framework.response import Response
from rest_framework import status
from .filters import SkillFilter
from django.shortcuts import get_object_or_404



class Skills(APIView):

    def get(self, request):
        queryset = SkillModel.objects.all()

        filterset = SkillFilter(data=request.query_params, queryset=queryset)

        serializer = SkillSerializer(instance=filterset.qs, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get(self, request, id):
        queryset = get_object_or_404(SkillModel, pk=id)

        serializer = SkillSerializer(instance=queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SkillSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, id):
        queryset = get_object_or_404(SkillModel, pk=id)

        serializer = SkillSerializer(instance=queryset, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        queryset = get_object_or_404(SkillModel, pk=id)

        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)