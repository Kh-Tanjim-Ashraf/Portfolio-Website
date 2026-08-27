from django.shortcuts import render
from .models import Skill as SkillModel
from rest_framework.views import APIView
from .serializers import SkillSerializer
from rest_framework.response import Response
from rest_framework import status
from .filters import SkillFilter



class Skill(APIView):

    def get(self, request):
        # print("="*50)
        # print("Query params:", request.query_params)
        # print("Query params:", request.query_params.getlist(key='ordering'))

        queryset = SkillModel.objects.all()

        filterset = SkillFilter(data=request.query_params, queryset=queryset)

        # print()

        # print("filterset:", filterset.qs)

        # for q in filterset.qs:
        #     # print(f'Skill: {q.name} ----- Proficiency: {q.proficiency} --- Display order: {q.display_order}')
        #     print(f'Skill: {q.name}')
        # print("="*50)

        serializer = SkillSerializer(instance=filterset.qs, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)