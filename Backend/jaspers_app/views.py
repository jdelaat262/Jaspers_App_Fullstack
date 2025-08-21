from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Deelnemer, Cursus
from .serializers import DeelnemerSerializer, CursusSerializer
from django.db import IntegrityError
from datetime import date, timedelta

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
        """
        deelnemer_data = request.data.copy()
        
        # Haal cursus-gerelateerde data uit de request als strings
        cursus_naam = deelnemer_data.get('cursus')
        cursus_datum_str = deelnemer_data.get('cursusdatum')
        refresher = deelnemer_data.get('refresher')
        geldigheid_jaren_str = deelnemer_data.get('geldigheid_jaren')
        geldigheid_datum_str = deelnemer_data.get('geldigheid_datum')

        # Converteer strings naar de juiste Python-typen (date of int)
        cursus_datum = date.fromisoformat(cursus_datum_str) if cursus_datum_str else None
        geldigheid_jaren = int(geldigheid_jaren_str) if geldigheid_jaren_str and geldigheid_jaren_str.isdigit() else None
        geldigheid_datum = date.fromisoformat(geldigheid_datum_str) if geldigheid_datum_str else None

        # --- BELANGRIJKE LOGICA HIER ---
        # Bepaal de definitieve geldigheid_datum als deze NIET expliciet is ingevoerd
        # en we WEL een cursusdatum en geldigheid_jaren hebben.
        if geldigheid_datum is None and cursus_datum and geldigheid_jaren is not None:
            # Bereken de verloopdatum door het aantal jaren bij het jaartal op te tellen
            geldigheid_datum = cursus_datum.replace(year=cursus_datum.year + geldigheid_jaren)
        # --- EINDE BELANGRIJKE LOGICA ---

        # Verwijder cursus-gerelateerde velden uit de deelnemer_data payload
        deelnemer_data.pop('cursus', None)
        deelnemer_data.pop('cursusdatum', None)
        deelnemer_data.pop('refresher', None)
        deelnemer_data.pop('geldigheid_jaren', None)
        deelnemer_data.pop('geldigheid_datum', None)

        try:
            # Zoek een bestaande Cursus op, of maak een nieuwe aan
            cursus_obj, created = Cursus.objects.get_or_create(
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

        # Koppel de aangemaakte of gevonden Cursus aan de Deelnemer-data
        deelnemer_data['cursus'] = cursus_obj.id

        # Valideer en sla de Deelnemer op
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
            continue # Sla deelnemers zonder gekoppelde cursus over

        expiration_date = None
        
        # Bepaal de verloopdatum
        if cursus.geldigheid_datum:
            expiration_date = cursus.geldigheid_datum
        elif cursus.cursusdatum and cursus.geldigheid_jaren is not None:
            # Converteer cursus.geldigheid_jaren naar een integer voordat je ermee rekent
            try:
                geldigheid_jaren_int = int(cursus.geldigheid_jaren)
                expiration_date = cursus.cursusdatum.replace(year=cursus.cursusdatum.year + geldigheid_jaren_int)
            except ValueError:
                # Handel het geval af dat geldigheid_jaren geen geldig getal is
                # Je kunt hier loggen of een foutmelding geven, maar voor nu slaan we deze over
                continue 

        if expiration_date and today <= expiration_date <= expiration_threshold:
            # Als het certificaat verloopt binnen de drempel, voeg toe aan de lijst
            deelnemer_serializer = DeelnemerSerializer(deelnemer)
            cursus_serializer = CursusSerializer(cursus)
            expiring_deelnemers.append({
                'deelnemer': deelnemer_serializer.data,
                'cursus': cursus_serializer.data,
                'verloopdatum': expiration_date.isoformat() # Verloopdatum toevoegen
            })
            
    return Response(expiring_deelnemers, status=status.HTTP_200_OK)

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
            # Haal de bestaande Cursus op
            cursus_obj = get_object_or_404(Cursus, pk=cursus_id)
        except Exception as e:
            return Response({"error": f"Cursus niet gevonden: {str(e)}"}, status=status.HTTP_404_NOT_FOUND)

        # Koppel de bestaande Cursus aan de Deelnemer-data
        deelnemer_data['cursus'] = cursus_obj.id

        # Verwijder de 'cursus_id' uit deelnemer_data, aangezien het model 'cursus' (ForeignKey) verwacht
        deelnemer_data.pop('cursus_id', None)

        serializer = self.get_serializer(data=deelnemer_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
