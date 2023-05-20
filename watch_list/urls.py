"""
Module to define the mapping of routes with their corresponding views.
"""

from django.urls import path
from .views import FetchSymbolsData


urlpatterns = [
    path('symbols-data', FetchSymbolsData.as_view(), name='fetch_symbols_data'),
]
