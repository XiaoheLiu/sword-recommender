from .models import Sword
import django_filters


class SwordFilter(django_filters.FilterSet):
    sword_type = django_filters.AllValuesFilter()
    manufacturer = django_filters.AllValuesFilter()
    name = django_filters.CharFilter(
        lookup_expr='icontains', label="Model Keywords")

    class Meta:
        model = Sword
        fields = [
            'manufacturer',
            'sword_type',
            'name',
        ]
