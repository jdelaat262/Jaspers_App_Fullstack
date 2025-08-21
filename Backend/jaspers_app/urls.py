from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Zorg ervoor dat alle views die je gebruikt, hier zijn geïmporteerd
from .views import CertificaatViewSet, ping_view, expiring_certificates_view, MobileDeelnemerViewSet 

# Maak een router-instantie aan
router = DefaultRouter()
# Registreer je CertificaatViewSet met een expliciete basename
router.register(r'certificaten', CertificaatViewSet, basename='certificaat') # <-- Expliciete basename
# Registreer je MobileDeelnemerViewSet met een expliciete basename
router.register(r'mobile-deelnemers', MobileDeelnemerViewSet, basename='mobile-deelnemer') # <-- Expliciete basename


urlpatterns = [
    # De router genereert nu automatisch de URL's voor je ViewSets
    path('', include(router.urls)), 
    
    # De ping_view blijft onveranderd
    path('ping/', ping_view, name='ping'),
    
    # Dit is het URL-patroon voor de herinneringen
    path('expiring-certificates/', expiring_certificates_view, name='expiring-certificates'), 
]
