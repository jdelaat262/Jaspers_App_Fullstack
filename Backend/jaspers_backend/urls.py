# jaspers_backend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dit importeert ALLE URL's van je jaspers_app
    path('', include('jaspers_app.urls')),
]