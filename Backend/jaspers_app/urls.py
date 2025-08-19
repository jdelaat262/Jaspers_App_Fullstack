# Jaspers_App/Backend/jaspers_app/urls.py

from django.urls import path
from .views import ping_view 
from .views import DeelnemerAPIView

urlpatterns = [
    path('deelnemer/', DeelnemerAPIView.as_view(), name='deelnemer-api'),
    path('ping/', ping_view, name='ping-pong'),
]