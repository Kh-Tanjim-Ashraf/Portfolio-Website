import django_filters
from .models import Skill, Project
from django.db.models import Q


class SkillFilter(django_filters.FilterSet):

    # `search` & `order` attributes/class-variables are actually the key of query params

    search = django_filters.CharFilter(method='filter_by_search')

    # `django_filters.OrderingFilter` fields anatomy: (query_value, model_field)
    # Note: The `query_value` comes from the query-parameter of the client request.

    ordering = django_filters.OrderingFilter(
        fields=(
            ('display_order', 'display_order'),
            ('proficiency', 'proficiency'),
        )
    )

    class Meta:
        model = Skill
        fields = ['name','category','proficiency','display_order','is_featured']

    # The `name` maps to the key of the query-param. In this case, the `search` keyword from that class attribute
    def filter_by_search(self, queryset, name, value):
        conditions = Q(name__icontains=value) | Q(category__icontains=value)

        try:
            int_value = int(value)
            conditions |= Q(proficiency=int_value)
            conditions |= Q(display_order=int_value)
        except ValueError:
            # If the user passes a string (ie. 'python'), then the logic of the interger conversion will be skipped
            pass

        # If the user types the special keyword `featured`, then the following condition will be applied; otherwise this condition will be skipped
        if value.lower() == 'featured':
            conditions |= Q(is_featured=True)

        return queryset.filter(conditions)



class ProjectFilter(django_filters.FilterSet):

    tech = django_filters.CharFilter(method='filter_by_tech', label='Filter by skill ID or name')

    search = django_filters.CharFilter(method='filter_by_search', label='Search by title, summary & description')

    ordering = django_filters.OrderingFilter(
        fields=(
            ('completed_date', 'completed_date'),
            ('display_order', 'display_order')
        )
    )

    class Meta:
        model = Project
        fields = ['category','is_featured']

    def filter_by_tech(self, queryset, name, value):
        '''
        Filter by **skill-id**/**skill-name** by using the `?tech=` query-param in the request
        '''
        if value.isdigit():
            conditions = Q(skill__id=int(value))
        else:
            conditions = Q(skill__name__icontains=value)

        return queryset.filter(conditions).distinct()

    def filter_by_search(self, queryset, name, value):
        '''
        Search by project title, summary & description
        '''
        conditions = Q(title__icontains=value) | Q(summary__icontains=value) | Q(description__icontains=value)

        return queryset.filter(conditions)