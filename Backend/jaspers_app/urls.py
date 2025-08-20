from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CertificaatViewSet, ping_view # Importeer de CertificaatViewSet en ping_view

# Maak een router-instantie aan
router = DefaultRouter()
# Registreer je CertificaatViewSet met de router
# Dit genereert automatisch URL's zoals /certificaten/ (lijst) en /certificaten/<pk>/ (detail)
router.register(r'certificaten', CertificaatViewSet)

urlpatterns = [
    # De router genereert nu automatisch de URL's voor je CertificaatViewSet
    # De basis-URL voor deze viewset is 'certificaten/'
    path('', include(router.urls)), 
    
    # De ping_view blijft onveranderd
    path('ping/', ping_view, name='ping'),
]
