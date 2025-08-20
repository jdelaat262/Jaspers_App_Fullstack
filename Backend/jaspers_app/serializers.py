from rest_framework import serializers
from .models import Deelnemer, Cursus

class CursusSerializer(serializers.ModelSerializer):
    """
    Serializer voor het Cursus-model.
    Zet Cursus-objecten om naar JSON en vice versa.
    """
    cursusdatum = serializers.DateField(allow_null=True, required=False)
    geldigheid_datum = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = Cursus
        fields = ['cursus', 'cursusdatum', 'refresher', 'geldigheid_jaren', 'geldigheid_datum']

class DeelnemerSerializer(serializers.ModelSerializer):
    """
    Serializer voor het Deelnemer-model.
    Zet Deelnemer-objecten om naar JSON en vice versa.
    """
    geboortedatum = serializers.DateField(allow_null=True, required=False)

    class Meta:
        model = Deelnemer
        fields = [
            'aanhef', 'voornaam', 'tussenvoegsel', 'achternaam',
            'bedrijfsnaam', 'email', 'geboortedatum', 'telefoonnummer',
            'windaId', 'notes',
            'cursus'
        ]
