from rest_framework import serializers
from decimal import Decimal
from .models import Pelicula


class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = '__all__'
        extra_kwargs = {
            'calificacion': {
                'max_value': Decimal('10.0'),
                'min_value': Decimal('0.0')
            }
        }