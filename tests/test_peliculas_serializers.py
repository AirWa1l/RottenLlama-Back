# tests/test_peliculas_serializers.py
import pytest
from decimal import Decimal
from peliculas.serializers import PeliculaSerializer

@pytest.mark.django_db
class TestPeliculaSerializer:
    def test_serializador_valido(self):
        """Prueba serialización con datos válidos"""
        data = {
            "titulo": "Interstellar",
            "fecha": 2014,
            "categoria": "ciencia ficcion",
            "calificacion": "8.6",  # Como string
            "director": "Christopher Nolan"
        }
        serializer = PeliculaSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        
        pelicula = serializer.save()
        assert pelicula.titulo == "Interstellar"
        assert pelicula.calificacion == Decimal('8.6')  # Comparación exacta

    def test_serializador_invalido(self):
        """Prueba con datos inválidos"""
        invalid_data = [
            {"titulo": "", "fecha": 2020, "calificacion": "8.5"},  # Título vacío
            {"titulo": "Sin calificación", "fecha": 2020},  # Falta calificación
            {"titulo": "Calif inválida", "fecha": 2020, "calificacion": "11.0"}  # > 10.0
        ]
        
        for data in invalid_data:
            serializer = PeliculaSerializer(data=data)
            assert not serializer.is_valid()
            assert "calificacion" in serializer.errors or "titulo" in serializer.errors