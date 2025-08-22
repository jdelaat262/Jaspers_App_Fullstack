from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CertificaatViewSet, ping_view, expiring_certificates_view, 
    MobileDeelnemerViewSet, generate_certificate_pdf, preview_certificate_html # <-- Alle views geïmporteerd
)

# Maak een router-instantie aan
router = DefaultRouter()
# Registreer je CertificaatViewSet met een expliciete basename
# Dit genereert URL's zoals /certificaten/ (lijst) en /certificaten/<pk>/ (detail)
router.register(r'certificaten', CertificaatViewSet, basename='certificaat')
# Registreer je MobileDeelnemerViewSet met een expliciete basename
# Dit genereert URL's zoals /mobile-deelnemers/ (lijst) en /mobile-deelnemers/<pk>/ (detail)
router.register(r'mobile-deelnemers', MobileDeelnemerViewSet, basename='mobile-deelnemer')

urlpatterns = [
    # De router genereert nu automatisch de URL's voor je ViewSets
    path('', include(router.urls)), 
    
    # URL voor de ping-test
    path('ping/', ping_view, name='ping'),
    
    # URL voor de lijst met verlopende certificaten
    path('expiring-certificates/', expiring_certificates_view, name='expiring-certificates'),
    
    # URL voor het genereren van een PDF-certificaat
    path('generate-certificate/<int:deelnemer_id>/', generate_certificate_pdf, name='generate-certificate-pdf'), 
    
    # URL voor de HTML-preview van het certificaat
    path('preview-certificate/<int:deelnemer_id>/', preview_certificate_html, name='preview-certificate-html'), 
]
