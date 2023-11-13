from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('houses/', ListHouses.as_view(), name='list_houses_page'),
    path('house/<slug:house_slug>/', AboutHouse.as_view(), name='about_house_page'),
]

# urlpatterns = [
#     path('', cache_page(60)(MainPage.as_view()), name='home'),
#     path('houses/', cache_page(3600)(AllHouses.as_view()), name='houses'),
#     path('house/<slug:house_slug>/', cache_page(3600)(EachHouse.as_view()), name='each_house'),
# ]