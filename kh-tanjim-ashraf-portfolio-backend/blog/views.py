from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostsSerializer
from rest_framework import status
from .filters import PostFilter
from rest_framework.permissions import AllowAny
from utils.custom_pagination import CustomPagination



class Posts(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        query_params = request.query_params
        
        # 1. Retrieve all the `Post` records along with it's associated data from the foreign tables; Remove duplicates by enforcing `distinct()` method; Mitigate inconsistency in results by enforcing `order_by('id')`, since `pagination` is used
        queryset = Post.objects.select_related('category','author').prefetch_related('tag').order_by('id').distinct()

        # 2. Check if the `query_param` dict is empty by using the `not` logical operator. If the dict is empty/falsy, then `not` will evaluate the conditional check as True
        if not query_params:
            # As no query-param is provided from the API client, display only the "PUBLISHED" posts regardless of the user being Anonymous/Admin
            queryset = queryset.filter(status='published')
        else:
            # As query-param exists, pass the queryset into the filtering process
            filterset = PostFilter(data=query_params, queryset=queryset, request=request)
            queryset = filterset.qs

        # 3. Instantiate pagination class with custom page-size
        paginator = CustomPagination(page_size=6)

        # 4. Paginate the filtered queryset
        paginated_queryset = paginator.paginate_queryset(queryset=queryset, request=request, view=self)
        
        # 5. Serialize the paginated queryset
        serializer = PostsSerializer(instance=paginated_queryset, many=True)

        # 6. Provide paginated response by wrapping the serialized data
        response = paginator.get_paginated_response(serializer.data)

        # 7. Include a status code
        response.status_code = status.HTTP_206_PARTIAL_CONTENT

        # 8. Return the paginated response
        return response