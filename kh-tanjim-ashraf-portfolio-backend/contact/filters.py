import django_filters

from .models import ContactMessage


class ContactsFilter(django_filters.FilterSet):

    class Meta:
        model = ContactMessage
        fields = ['is_read']