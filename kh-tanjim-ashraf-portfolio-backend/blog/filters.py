import django_filters
from .models import Post
from django.utils.text import slugify



class PostFilter(django_filters.FilterSet):

    status = django_filters.CharFilter(method='filter_by_status', label='Filter by post status (Draft, published, all)')
    category = django_filters.CharFilter(method='filter_by_category', label='Filter by category slug')
    tag = django_filters.CharFilter(method='filter_by_tags', label='Filter by tag slug; Multiple tags accepted (comma-separated)')

    class Meta:
        model = Post
        fields = ['is_featured']

    def isAdmin(self):
        '''
        Classify if the user is authenticated and have administrative privileges
        '''
        user = self.request.user
        return user.is_authenticated and user.is_superuser

    def filter_by_user_permission(self, queryset, queryParamName, value):
        '''
        Filter out & return only the "Published" posts to anonymous users, otherwise return all matched records for admin.
        '''

        # Implement dynamic keyword argument using dictionary unpacking (**)
        lookup = {queryParamName:value}

        if self.isAdmin():
            return queryset.filter(**lookup)
        else:
            return queryset.filter(status='published', **lookup)


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
            return self.filter_by_user_permission(queryset, 'tag__slug__in', value).distinct()  # Remove duplicates
        else:
            value = slugify(value)
            return self.filter_by_user_permission(queryset, 'tag__slug', value).distinct()