"""
Module to define the mapping of routes with their corresponding views.
"""

from django.urls import path
from .views import RegisterUserAPIView, LoginView


urlpatterns = [
    path('register', RegisterUserAPIView.as_view(), name='register_user'),
    path('login', LoginView.as_view(), name='login_user'),
]
