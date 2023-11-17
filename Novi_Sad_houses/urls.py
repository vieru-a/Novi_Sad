from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('houses/', cache_page(3600)(ListHouses.as_view()), name='list_houses_page'),
    path('house/<slug:house_slug>/', cache_page(3600)(AboutHouse.as_view()), name='about_house_page'),
]
