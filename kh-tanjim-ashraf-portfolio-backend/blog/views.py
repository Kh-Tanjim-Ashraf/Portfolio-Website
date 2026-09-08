from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, PostLikeViewCount
from .serializers import PostsSerializer, PostMinimalSerializer, PostLikeSerializer
from rest_framework import status
from .filters import PostFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.custom_pagination import CustomPagination
from django.core.cache import cache
from django.db.models import F
from django.db import IntegrityError



class Posts(APIView):

    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]

        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

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

    def post(self, request):
        serializer = PostsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)



class PostDetail(APIView):

    def get_permissions(self):
        SAFE_METHODS = ['GET']
        
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def isAdmin(self):
        user = self.request.user
        return user.is_authenticated and user.is_superuser

    def get(self, request, slug):
        # Required: Redis
        try:
            queryset = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response(data={'error': 'No post found!'}, status=status.HTTP_404_NOT_FOUND)

        # Throw a 404 Not Found error if an anonymous user wants to view a post with `status=draft`
        if queryset.status == 'draft' and not self.isAdmin():
            return Response(data={"error":"No post found!"}, status=status.HTTP_404_NOT_FOUND)

        visitor_id = request.META.get('HTTP_X_VISITOR_ID')

        # Note: The post's view count will be updated only if a 'visitor_id' exists & passes the cooldown check mechanism. Admin/owner of the post will not have the `X-Visitor-Id` header
        if visitor_id:
            cache_key = f"viewed_post_{queryset.id}_{visitor_id}"

            # Update `views_count` if key doesn't exist in cache
            if not cache.get(cache_key):
                PostLikeViewCount.objects.filter(post=queryset).update(views_count=F('views_count') + 1)

                # Reload the old object with new field values from database to inside the memory
                queryset.refresh_from_db()

                # Set a cache key in Redis with boolean value (used in cooldown check later) for a day
                cache.set(cache_key, True, timeout=86400)
            
        # Admin privilege to view draft posts
        serializer = PostsSerializer(instance=queryset)

        related_posts = queryset.category.posts.all()

        related_posts_serialized = PostMinimalSerializer(instance=related_posts, many=True)

        data = {
            'Post': serializer.data,
            'Related Posts': related_posts_serialized.data
        }
        
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        try:
            queryset = Post.objects.get(slug=slug)
            serializer = PostsSerializer(instance=queryset, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            data = {"message": "No post found!"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug):
        try:
            queryset = Post.objects.get(slug=slug)
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            data = {"message": "No post found!"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)



class PostLike(APIView):

    permission_classes = [AllowAny]

    def post(self, request, slug):
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response(data={'message': 'No post found!'}, status=status.HTTP_404_NOT_FOUND)

        # Check if `X-Visitor-Id` exists in the request-header
        visitor_id = request.META.get('HTTP_X_VISITOR_ID')

        if not visitor_id:
            data = {"message": "'X-Visitor-Id' is missing in the Request header."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PostLikeSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save(post=post, visitor_id=visitor_id)
            except IntegrityError:
                data = {"message": "Post-like with this Post and Visitor id already exists."}
                return Response(data=data, status=status.HTTP_409_CONFLICT)
            
            data = {'data': serializer.data, 'liked': True}
            return Response(data=data, status=status.HTTP_201_CREATED)