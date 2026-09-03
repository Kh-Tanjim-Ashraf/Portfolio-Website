from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostsSerializer
from rest_framework import status
from .filters import PostFilter
from rest_framework.permissions import AllowAny



class Posts(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        query_params = request.query_params
        
        # 1. Retrieve all the `Post` records along with it's associated data from the foreign tables
        queryset = Post.objects.select_related('category','author').prefetch_related('tag').all()

        # 2. Check if the query_param dict is empty by using the `not` logical operator
        if not query_params:
            # Filter out & display only the "PUBLISHED" posts regardless of anonymous user & admin
            queryset = queryset.filter(status='published')
        else:
            # Pass the queryset into the filtering process if any query-param exists
            filterset = PostFilter(data=query_params, queryset=queryset, request=request)
            queryset = filterset.qs

        serializer = PostsSerializer(instance=queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)