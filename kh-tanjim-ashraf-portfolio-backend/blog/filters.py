import django_filters
from .models import Post



class PostFilter(django_filters.FilterSet):

    status = django_filters.CharFilter(method='filter_by_status', label='Filter by post status')

    class Meta:
        model = Post
        fields = []

    # `name=status` & `value=<value of the query-param>`
    def filter_by_status(self, queryset, name, value):
        user = self.request.user
        value = value.lower()
        
        owner_privileged_status_query = ['draft','all']

        # For admin
        if user.is_authenticated \
            and user.is_superuser \
            and value in owner_privileged_status_query:

            # For draft posts
            if value == owner_privileged_status_query[0]:
                return queryset.filter(status=value)
                
            # For all posts
            if value == owner_privileged_status_query[1]:
                return queryset
        
        # For anonymous users: If uses the `?status=` query-param with whether "draft/all" query-value, but will only get the "Published" posts
        return queryset.filter(status='published')