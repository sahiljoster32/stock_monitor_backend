"""
Module to config the admin panel for users app.
"""

from django.contrib import admin
from .models import WatchList

admin.site.register(WatchList)
