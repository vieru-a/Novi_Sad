from pathlib import Path

from django.views.generic import ListView, DetailView
from django_filters.views import FilterView

from .filters import HouseFilter
from .models import *

import os
import random

BASE_DIR = Path(__file__).resolve().parent.parent
houses_count = len(os.listdir(BASE_DIR / f'templates/static/assets/media'))


class MainPage(ListView):
    model = House
    template_name = 'main_page.html'
    context_object_name = 'data'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добро пожаловать в Нови Сад'
        return context

    def get_queryset(self):
        random_houses = random.sample(range(1, houses_count), 9)
        return House.objects.filter(pk__in=random_houses, is_published=True).prefetch_related("houseimage_set")


class ListHouses(FilterView):
    model = House
    template_name = 'list_houses_page.html'
    context_object_name = 'data'
    paginate_by = 15
    queryset = House.objects.all().prefetch_related("houseimage_set")
    filterset_class = HouseFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Недвижимость в городе Нови Сад и его окрестностях'
        context['min_price'] = self.request.GET.get('min_price')
        context['max_price'] = self.request.GET.get('max_price')
        context['ordering'] = self.request.GET.get('ordering')
        return context


class AboutHouse(DetailView):
    model = House
    template_name = 'about_house_page.html'
    context_object_name = 'd'
    slug_url_kwarg = 'house_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Дом: {context["d"].title} - {context["d"].price}€'
        return context
