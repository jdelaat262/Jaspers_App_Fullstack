# Jaspers_App/Backend/jaspers_app/urls.py

from django.urls import path
from .views import ping_view

urlpatterns = [
    path('ping/', ping_view, name='ping-pong'),
]