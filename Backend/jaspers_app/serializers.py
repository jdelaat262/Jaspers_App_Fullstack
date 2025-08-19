from rest_framework import serializers
from .models import Deelnemer

class DeelnemerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deelnemer
        fields = '__all__'