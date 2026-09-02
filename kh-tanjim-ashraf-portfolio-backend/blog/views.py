from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostsSerializer
from rest_framework import status



class Posts(APIView):

    def get(self, request):
        queryset = Post.objects.select_related('category','author').prefetch_related('tag').all()

        serializer = PostsSerializer(instance=queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)