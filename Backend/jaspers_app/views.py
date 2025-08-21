from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Deelnemer, Cursus
from .serializers import DeelnemerSerializer, CursusSerializer
from django.db import IntegrityError
from datetime import date, timedelta
from django.shortcuts import get_object_or_404

# Importeer WeasyPrint gerelateerde functies
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings # <-- NIEUWE IMPORT: Nodig om STATIC_URL te gebruiken

class CertificaatViewSet(viewsets.ModelViewSet):
    """
    Deze ViewSet handelt het aanmaken van zowel Cursus- als Deelnemer-objecten af
    op basis van één gecombineerd formulier.
    """
    queryset = Deelnemer.objects.all()
    serializer_class = DeelnemerSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom create-methode om zowel Cursus als Deelnemer aan te maken en te koppelen.
        Als een deelnemer al bestaat (op basis van achternaam en geboortedatum),
        wordt de nieuwe cursus aan die bestaande deelnemer gekoppeld.
        """
        deelnemer_data = request.data.copy()
        
        cursus_naam = deelnemer_data.get('cursus')
        cursus_datum_str = deelnemer_data.get('cursusdatum')
        refresher = deelnemer_data.get('refresher')
        geldigheid_jaren_str = deelnemer_data.get('geldigheid_jaren')
        geldigheid_datum_str = deelnemer_data.get('geldigheid_datum')

        cursus_datum = date.fromisoformat(cursus_datum_str) if cursus_datum_str else None
        geldigheid_jaren = int(geldigheid_jaren_str) if geldigheid_jaren_str and geldigheid_jaren_str.isdigit() else None
        geldigheid_datum = date.fromisoformat(geldigheid_datum_str) if geldigheid_datum_str else None

        if geldigheid_datum is None and cursus_datum and geldigheid_jaren is not None:
            geldigheid_datum = cursus_datum.replace(year=cursus_datum.year + geldigheid_jaren)
        
        deelnemer_data.pop('cursus', None)
        deelnemer_data.pop('cursusdatum', None)
        deelnemer_data.pop('refresher', None)
        deelnemer_data.pop('geldigheid_jaren', None)
        deelnemer_data.pop('geldigheid_datum', None)

        try:
            cursus_obj, created_cursus = Cursus.objects.get_or_create(
                cursus=cursus_naam,
                cursusdatum=cursus_datum,
                refresher=refresher,
                geldigheid_jaren=geldigheid_jaren,
                geldigheid_datum=geldigheid_datum
            )
        except IntegrityError:
            return Response({"error": "Cursus met deze gegevens bestaat al."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Fout bij aanmaken cursus: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        achternaam = deelnemer_data.get('achternaam')
        geboortedatum_str = deelnemer_data.get('geboortedatum')
        geboortedatum = date.fromisoformat(geboortedatum_str) if geboortedatum_str else None

        if achternaam and geboortedatum:
            try:
                deelnemer_obj = Deelnemer.objects.get(
                    achternaam=achternaam,
                    geboortedatum=geboortedatum
                )
                deelnemer_obj.cursus = cursus_obj
                deelnemer_obj.save()
                
                serializer = self.get_serializer(deelnemer_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Deelnemer.DoesNotExist:
                pass
            except Exception as e:
                return Response({"error": f"Fout bij zoeken deelnemer: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        deelnemer_data['cursus'] = cursus_obj.id

        serializer = self.get_serializer(data=deelnemer_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
def ping_view(request):
    """
    Een eenvoudige view om de verbinding met de backend te testen.
    """
    return Response({'message': 'Hello world, de backend is verbonden!'})

@api_view(['GET'])
def expiring_certificates_view(request):
    """
    Haalt deelnemers op waarvan het certificaat binnen 28 dagen verloopt.
    """
    today = date.today()
    expiration_threshold = today + timedelta(days=28)
    
    expiring_deelnemers = []

    for deelnemer in Deelnemer.objects.all():
        cursus = deelnemer.cursus
        if not cursus:
            continue

        expiration_date = None
        
        if cursus.geldigheid_datum:
            expiration_date = cursus.geldigheid_datum
        elif cursus.cursusdatum and cursus.geldigheid_jaren is not None:
            try:
                geldigheid_jaren_int = int(cursus.geldigheid_jaren)
                expiration_date = cursus.cursusdatum.replace(year=cursus.cursusdatum.year + geldigheid_jaren_int)
            except ValueError:
                continue 

        if expiration_date and today <= expiration_date <= expiration_threshold:
            deelnemer_serializer = DeelnemerSerializer(deelnemer)
            cursus_serializer = CursusSerializer(cursus)
            expiring_deelnemers.append({
                'deelnemer': deelnemer_serializer.data,
                'cursus': cursus_serializer.data,
                'verloopdatum': expiration_date.isoformat()
            })
            
    return Response(expiring_deelnemers, status=status.HTTP_200_OK)

# NIEUWE VIEW VOOR CERTIFICAAT GENERATIE
@api_view(['GET'])
def generate_certificate_pdf(request, deelnemer_id):
    """
    Genereert een PDF-certificaat voor een specifieke deelnemer.
    """
    try:
        deelnemer = get_object_or_404(Deelnemer, pk=deelnemer_id)
        cursus = deelnemer.cursus # Haal de gekoppelde cursus op
        
        if not cursus:
            return HttpResponse("Geen cursus gevonden voor deze deelnemer.", status=404)

        # Context voor de template
        context = {
            'deelnemer': deelnemer,
            'cursus': cursus,
        }

        # Render de HTML-template met de context
        html_string = render_to_string('certificaat_template.html', context)
        
        # Converteer de HTML naar PDF met WeasyPrint
        # BELANGRIJK: Geef base_url mee zodat WeasyPrint statische bestanden kan vinden
        pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri(settings.STATIC_URL)).write_pdf()

        # Creëer de HTTP-respons
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificaat_{deelnemer.voornaam}_{deelnemer.achternaam}.pdf"'
        return response

    except Deelnemer.DoesNotExist:
        return HttpResponse("Deelnemer niet gevonden.", status=404)
    except Exception as e:
        return HttpResponse(f"Fout bij het genereren van het certificaat: {str(e)}", status=500)

# Nieuwe ViewSet voor het verwerken van mobiele formulieren via QR-code
class MobileDeelnemerViewSet(viewsets.ModelViewSet):
    """
    Deze ViewSet handelt het aanmaken van Deelnemer-objecten af
    die gekoppeld worden aan een reeds bestaande Cursus (via QR-code).
    """
    queryset = Deelnemer.objects.all()
    serializer_class = DeelnemerSerializer

    def create(self, request, *args, **kwargs):
        deelnemer_data = request.data.copy()
        cursus_id = deelnemer_data.get('cursus_id') # Verwacht cursus ID van mobiele formulier

        if not cursus_id:
            return Response({"error": "Cursus ID is vereist."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cursus_obj = get_object_or_404(Cursus, pk=cursus_id)
        except Exception as e:
            return Response({"error": f"Cursus niet gevonden: {str(e)}"}, status=status.HTTP_404_NOT_FOUND)

        # Koppel de bestaande Cursus aan de Deelnemer-data
        deelnemer_data['cursus'] = cursus_obj.id

        deelnemer_data.pop('cursus_id', None)

        serializer = self.get_serializer(data=deelnemer_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
