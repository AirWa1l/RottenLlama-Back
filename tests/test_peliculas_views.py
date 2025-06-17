# tests/test_peliculas_views.py
import pytest
from rest_framework.test import APIRequestFactory
from peliculas.models import Pelicula
from peliculas.views import PeliculasPopularesView, PeliculaPorCategoriaView

@pytest.mark.django_db
class TestPeliculaViews:
    def setup_method(self):
        self.factory = APIRequestFactory()
        # Crear datos de prueba
        self.pelicula1 = Pelicula.objects.create(
            titulo="Inception",
            categoria="ciencia ficcion",
            fecha=2010,
            calificacion=8.8,
            director="Christopher Nolan"
        )
        self.pelicula2 = Pelicula.objects.create(
            titulo="The Shawshank Redemption",
            categoria="drama",
            fecha=1994,
            calificacion=9.3,
            director="Frank Darabont"
        )

    def test_peliculas_populares_view(self):
        request = self.factory.get('/peliculas/populares/')
        view = PeliculasPopularesView.as_view()
        response = view(request)
        
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["titulo"] == "The Shawshank Redemption"

    def test_pelicula_por_categoria_view(self):
        request = self.factory.get('/peliculas/categoria/', {'categoria': 'drama'})
        view = PeliculaPorCategoriaView.as_view()
        response = view(request)
        
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["titulo"] == "The Shawshank Redemption"

    def test_pelicula_por_categoria_vacia(self):
        request = self.factory.get('/peliculas/categoria/', {'categoria': 'inexistente'})
        view = PeliculaPorCategoriaView.as_view()
        response = view(request)
        
        assert response.status_code == 404
        assert response.data["mensaje"] == "No se encontraron películas en esta categoría."
