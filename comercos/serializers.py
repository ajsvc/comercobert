
from .models import Establiment
from rest_framework import serializers



class EstablimentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Establiment
        fields = ('pk', 'nom', 'telefon', 'email', 'adreca', 'latitude', 'longitude')