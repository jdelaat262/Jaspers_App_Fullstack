# jaspers_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CertificaatViewSet, ping_view, expiring_certificates_view,
    MobileDeelnemerViewSet, generate_certificate_pdf, preview_certificate_html
)

# Maak een router-instantie aan
router = DefaultRouter()
# Registreer je ViewSets
router.register(r'certificaten', CertificaatViewSet, basename='certificaat')
router.register(r'mobile-deelnemers', MobileDeelnemerViewSet, basename='mobile-deelnemer')

urlpatterns = [
    # Routerpaden
    path('api/v1/', include(router.urls)), 
    
    # Handmatige paden
    path('api/v1/ping/', ping_view, name='ping'),
    path('api/v1/expiring-certificates/', expiring_certificates_view, name='expiring-certificates'),
    
    # De paden die de foutmelding veroorzaken
    path('api/v1/generate-certificate/<int:deelnemer_id>/<int:cursus_id>/', generate_certificate_pdf, name='generate-certificate-pdf'), 
    path('api/v1/preview-certificate/<int:deelnemer_id>/<int:cursus_id>/', preview_certificate_html, name='preview-certificate-html'), 
]