from django_filters import FilterSet, NumberFilter, ChoiceFilter

from .models import *


class HouseFilter(FilterSet):
    min_price = NumberFilter(field_name="price", label='Минимальная цена', lookup_expr='gte')
    max_price = NumberFilter(field_name="price", label='Максимальная цена', lookup_expr='lte')
    ordering = ChoiceFilter(method='filter_by_order', label='Сортировать по', choices=[
        ['price', 'по увеличению цены'],
        ['-price', 'по уменьшению цены'],
        ['m2', 'по увеличению площади'],
        ['-m2', 'по уменьшению площади']])

    class Meta:
        model = House
        fields = ['min_price', 'max_price', 'ordering', ]

    def filter_by_order(self, queryset, name, value):
        expression = ''
        li = ['price', '-price', 'm2', '-m2']
        if value in li:
            expression = value
        return queryset.order_by(expression)
