import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from peliculas.models import Pelicula

@pytest.mark.django_db
class TestPeliculaEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        # Prefijo '/api/' añadido a todas las rutas
        self.base_url = '/api/'
        
        # Datos de prueba
        self.pelicula1 = Pelicula.objects.create(
            titulo="Inception",
            categoria="ciencia ficcion",
            fecha=2010,
            calificacion=Decimal('8.8'),
            director="Christopher Nolan"
        )

    def test_listado_peliculas(self):
        response = self.client.get(f"{self.base_url}peliculas/")
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_peliculas_populares(self):
        response = self.client.get(f"{self.base_url}peliculas/populares/")
        assert response.status_code == 200
        assert len(response.json()) >= 1

@pytest.mark.django_db
class TestPeliculaCRUD:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.base_url = '/api/'
        
    def test_actualizacion_pelicula(self):
        pelicula = Pelicula.objects.create(
            titulo="Original",
            categoria="drama",
            fecha=2020,
            calificacion=Decimal('5.0'),
            director="Director X"
        )
        response = self.client.patch(
            f"{self.base_url}peliculas/{pelicula.id}/",
            {"titulo": "Actualizada"},
            format='json'
        )
        assert response.status_code == 200
        assert Pelicula.objects.get(id=pelicula.id).titulo == "Actualizada"