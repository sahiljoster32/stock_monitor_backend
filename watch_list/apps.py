"""
Module that defines the configs of watch_list app.
"""

from django.apps import AppConfig


class WatchListConfig(AppConfig):
    """
    Class defining the configs of watch_list app.

    Attributes:
        default_auto_field: Defining the default auto field in django db.
        name: Name of the app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'watch_list'
