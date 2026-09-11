import django_filters
from .models import Post, Comment
from django.utils.text import slugify
from django.db.models import Q



class PostFilter(django_filters.FilterSet):

    status = django_filters.CharFilter(method='filter_by_status', label='Filter by post status (Draft, published, all)')
    category = django_filters.CharFilter(method='filter_by_category', label='Filter by category slug')
    tag = django_filters.CharFilter(method='filter_by_tags', label='Filter by tag slug; Multiple tags accepted (comma-separated)')
    search = django_filters.CharFilter(method='filter_by_search', label='Search by post\'s title, excerpt & content')
    ordering = django_filters.OrderingFilter(
        fields=(
            # ('ORM path', 'API query parameter name')
            ('published_at', 'published_at'),
            ('likesNviews__views_count', 'views_count'),
            ('likesNviews__likes_count', 'likes_count'),
            ('title', 'title'),
        )
    )

    class Meta:
        model = Post
        fields = ['is_featured']

    def isAdmin(self):
        '''
        Classify if the user is authenticated and have administrative privileges
        '''
        user = self.request.user
        return user.is_authenticated and user.is_superuser

    def filter_by_user_permission(self, queryset, query_param_name=None, value=None, lookup_required=True):
        '''
        Filter out & return only the "Published" posts to anonymous users, otherwise return all matched records for admin.
        '''

        # Implement dynamic keyword argument using dictionary unpacking (**)
        lookup = {query_param_name:value}

        if self.isAdmin():
            return queryset.filter(**lookup) if lookup_required else queryset
        else:
            return queryset.filter(status='published', **lookup) if lookup_required else queryset.filter(status='published')

    # `name=status` & `value=<value of the query-param>`
    def filter_by_status(self, queryset, name, value):
        value = value.lower()
        
        admin_privileged_status_query = ['draft','all']

        # For admin
        if self.isAdmin() and value in admin_privileged_status_query:

            # For draft posts
            if value == admin_privileged_status_query[0]:
                return queryset.filter(status=value)
                
            # For all posts
            if value == admin_privileged_status_query[1]:
                return queryset
        
        # For anonymous users: If uses the `?status=` query-param with whether "draft/all" query-value, but will only get the "Published" posts
        return queryset.filter(status='published')

    def filter_by_category(self, queryset, name, value):
        # Slugify the category value to ensure extra security
        value = slugify(value)

        # The `name` is the name of the query-param
        return self.filter_by_user_permission(queryset, 'category__slug', value)

    def filter_by_tags(self, queryset, name, value):
        '''
        Both single tag & comma-separated tags are handled
        '''
        
        # Check if multiple comma-separated tag-values are sent from the API client
        if len(value.split(',')) > 1:
            value_list = [val.strip() for val in value.split(',') if val.strip()]
            
            # If the list is empty
            if not value_list:
                return queryset

            # Slugify each value of the list
            value = [slugify(val) for val in value_list]
            return self.filter_by_user_permission(queryset, 'tag__slug__in', value)
        else:
            value = slugify(value)
            return self.filter_by_user_permission(queryset, 'tag__slug__icontains', value)

    def filter_by_search(self, queryset, name, value):
        '''
        Search by post's title, excerpt & content (content_markdown)
        '''
        value = value.strip().lower()

        # Magic keyword for `?search=featured` query-param
        if value == 'featured':
            return queryset.filter(is_featured=True)

        queryset = queryset.filter(
            Q(title__icontains=value)
            | Q(excerpt__icontains=value)
            | Q(content_markdown__icontains=value)
        )

        return self.filter_by_user_permission(queryset, lookup_required=False)



class CommentFilter(django_filters.FilterSet):

    post = django_filters.CharFilter(method='filter_by_post', label='Filter by post slug')

    class Meta:
        model = Comment
        fields = ['is_approved']

    def filter_by_post(self, queryset, name, value):
        return queryset.filter(post__slug__icontains=value)