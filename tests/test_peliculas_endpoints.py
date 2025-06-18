# tests/test_peliculas_endpoints.py
import pytest
from rest_framework.test import APIClient
from peliculas.models import Pelicula

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def setup_peliculas():
    # Datos de prueba para múltiples tests
    pelicula1 = Pelicula.objects.create(
        titulo="Inception",
        categoria="ciencia ficcion",
        fecha=2010,
        calificacion=8.8,
        director="Christopher Nolan"
    )
    pelicula2 = Pelicula.objects.create(
        titulo="The Shawshank Redemption",
        categoria="drama",
        fecha=1994,
        calificacion=9.3,
        director="Frank Darabont"
    )
    pelicula3 = Pelicula.objects.create(
        titulo="Madagascar",
        categoria="animacion",
        fecha=2005,
        calificacion=6.9,
        director="Eric Darnell"
    )
    return [pelicula1, pelicula2, pelicula3]

@pytest.mark.django_db
class TestPeliculaEndpoints:
    def test_listado_peliculas(self, client, setup_peliculas):
        response = client.get("/api/peliculas/")
        assert response.status_code == 200
        assert len(response.data) == 3
        assert response.data[0]["titulo"] == "Inception"

    def test_filtro_por_categoria(self, client, setup_peliculas):
        response = client.get("/api/peliculas/categoria/?categoria=ciencia ficcion")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["titulo"] == "Inception"

    def test_filtro_categoria_no_existente(self, client, setup_peliculas):
        response = client.get("/api/peliculas/categoria/?categoria=no_existe")
        assert response.status_code == 404
        assert response.data["mensaje"] == "No se encontraron películas en esta categoría."

    def test_peliculas_recientes(self, client, setup_peliculas):
        response = client.get("/api/peliculas/recientes/")
        assert response.status_code == 200
        assert len(response.data) == 3
        assert response.data[0]["titulo"] == "Inception"  # Más reciente

    def test_detalle_pelicula(self, client, setup_peliculas):
        pelicula = setup_peliculas[0]
        response = client.get(f"/api/peliculas/{pelicula.id}/")
        assert response.status_code == 200
        assert response.data["titulo"] == "Inception"

    def test_eliminar_pelicula(self, client, setup_peliculas):
        pelicula = setup_peliculas[0]
        response = client.delete(f"/api/peliculas/{pelicula.id}/")
        assert response.status_code == 204
        assert Pelicula.objects.count() == 2