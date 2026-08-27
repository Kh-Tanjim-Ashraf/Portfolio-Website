import django_filters
from .models import Skill
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
        # print("query-key-name:", name)
        # print("search-query-value:", value)
        
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

        # print("conditions:", conditions)
        
        result = queryset.filter(conditions)

        # print("result", result)

        return result