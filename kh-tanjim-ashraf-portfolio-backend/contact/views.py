from typing import Sequence

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ContactMessage
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ContactsSerializer, ContactsDetailSerializer


class Contacts(APIView):

    def get_permissions(self):
        SAFE_METHODS = ['POST']

        if self.request.method in SAFE_METHODS:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def get(self, request):
        queryset = ContactMessage.objects.order_by('-created_at')

        serializer = ContactsDetailSerializer(instance=queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ContactsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class ContactDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            queryset = ContactMessage.objects.get(id=id)

            serializer = ContactsDetailSerializer(instance=queryset)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except ContactMessage.DoesNotExist:

            return Response(data={"message": "No contact message found!"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            queryset = ContactMessage.objects.get(id=id)

            serializer = ContactsDetailSerializer(instance=queryset, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

        except ContactMessage.DoesNotExist:
            return Response(data={"message": "No contact message found!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            queryset = ContactMessage.objects.get(id=id)

            queryset.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except ContactMessage.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)