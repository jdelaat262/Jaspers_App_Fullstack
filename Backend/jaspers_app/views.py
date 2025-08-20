from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Deelnemer, Cursus
from .serializers import DeelnemerSerializer, CursusSerializer
from django.db import IntegrityError

class CertificaatViewSet(viewsets.ModelViewSet):
    """
    Deze ViewSet handelt het aanmaken van zowel Cursus- als Deelnemer-objecten af
    op basis van één gecombineerd formulier.
    """
    queryset = Deelnemer.objects.all() # We gebruiken Deelnemer als basis queryset
    serializer_class = DeelnemerSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom create-methode om zowel Cursus als Deelnemer aan te maken en te koppelen.
        """
        deelnemer_data = request.data.copy()
        
        # Haal cursus-gerelateerde data uit de request
        cursus_naam = deelnemer_data.get('cursus')
        cursus_datum = deelnemer_data.get('cursusdatum')
        refresher = deelnemer_data.get('refresher')
        geldigheid_jaren = deelnemer_data.get('geldigheid_jaren')
        geldigheid_datum = deelnemer_data.get('geldigheid_datum')

        # Verwijder cursus-gerelateerde velden uit de deelnemer_data payload
        # Deze velden horen bij het Cursus-model, niet direct bij Deelnemer
        deelnemer_data.pop('cursus', None)
        deelnemer_data.pop('cursusdatum', None)
        deelnemer_data.pop('refresher', None)
        deelnemer_data.pop('geldigheid_jaren', None)
        deelnemer_data.pop('geldigheid_datum', None)

        try:
            # Zoek een bestaande Cursus op, of maak een nieuwe aan
            # Dit voorkomt duplicatie van cursusgegevens
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
        serializer.is_valid(raise_exception=True) # Gooi een fout als validatie mislukt
        self.perform_create(serializer) # Sla het Deelnemer-object op
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
def ping_view(request):
    """
    Een eenvoudige view om de verbinding met de backend te testen.
    """
    return Response({'message': 'Hello world, de backend is verbonden!'})
