import django_filters
from .models import Location


class LocationFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')
    average_rating = django_filters.NumberFilter(field_name='average_rating', method='filter_by_avg_rating')

    class Meta:
        model = Location
        fields = ['title', 'description', 'category', 'average_rating']

    def filter_by_avg_rating(self, queryset, name, value):
        return queryset.filter(average_rating__gte=value)
