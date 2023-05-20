"""
Module that defines the configs of users app.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Class defining the configs of users app.

    Attributes:
        default_auto_field: Defining the default auto field in django db.
        name: Name of the app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
