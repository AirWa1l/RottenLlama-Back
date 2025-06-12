from django.test import TestCase

# peliculas/tests.py
import pytest
from peliculas.models import Pelicula

@pytest.mark.django_db
def test_crear_pelicula():
    pelicula = Pelicula.objects.create(titulo="Inception", categoria="ciencia ficcion", fecha=2010,calificacion=5, director="Christopher Nolan")
    assert pelicula.titulo == "Inception"
    assert pelicula.categoria == "ciencia ficcion"
    assert pelicula.fecha == 2010
    assert pelicula.calificacion == 5
    assert pelicula.director=="Christopher Nolan"
    
    pelicula = Pelicula.objects.create(titulo="madagascar", categoria="comedia", fecha=2005,calificacion=4, director="Eric Darnell")
    assert pelicula.titulo == "madagascar"
    assert pelicula.categoria == "comedia"
    assert pelicula.fecha == 2005
    assert pelicula.calificacion == 4
    assert pelicula.director=="Eric Darnell"

from rest_framework.test import APIClient

@pytest.mark.django_db
def test_endpoint_con_apiclient():
    client = APIClient()

    # Crear una película
    from peliculas.models import Pelicula
    Pelicula.objects.create(
        titulo="Inception",
        categoria="ciencia ficcion",
        fecha=2010,
        calificacion=5,
        director="Christopher Nolan"
    )
    
    Pelicula.objects.create(
        titulo="madagascar",
        categoria="comedia",
        fecha=2005,
        calificacion=4,
        director="Eric Darnell"
    )
    # Hacer GET al endpoint
    response = client.get("/api/peliculas/")
    assert response.status_code == 200
    assert response.data[0]["titulo"] == "Inception"
    assert response.data[1]["titulo"] == "madagascar"

import pytest
from rest_framework.test import APIClient
from peliculas.models import Pelicula

@pytest.mark.django_db
def test_peliculas_populares_endpoint():
    # Crear datos de prueba
    Pelicula.objects.create(
        titulo="Inception",
        categoria="ciencia ficcion",
        fecha=2010,
        calificacion=5,
        director="Christopher Nolan"
    )
    Pelicula.objects.create(
        titulo="madagascar",
        categoria="comedia",
        fecha=2005,
        calificacion=4,
        director="Eric Darnell"
    )

    client = APIClient()

    response = client.get("/api/peliculas/populares/")

    assert response.status_code == 200

    data = response.json()

    # Aseguramos que devuelve al menos una película
    assert len(data) >= 1

    # Verificamos que solo las películas con buena calificación están incluidas
    for pelicula in data:
        assert float(pelicula["calificacion"]) >= 4
        
import pytest                # asegúrate de tener esto
from rest_framework.test import APIClient
from peliculas.models import Pelicula

@pytest.mark.django_db       # ← aquí
def test_peliculas_por_categoria_endpoint():
    # Crear datos de prueba
    Pelicula.objects.create(
        titulo="Madagascar",
        categoria="comedia",
        fecha=2005,
        calificacion=4,
        director="Eric Darnell"
    )
    Pelicula.objects.create(
        titulo="Inception",
        categoria="ciencia ficcion",
        fecha=2010,
        calificacion=5,
        director="Christopher Nolan"
    )

    client = APIClient()

    # Consultar películas por categoría "comedia"
    response = client.get("/api/peliculas/categoria/?categoria=comedia")
    assert response.status_code == 200

    data = response.json()

    # Asegurar que al menos una película fue devuelta
    assert len(data) >= 1

    # Asegurar que todas las películas son de la categoría "comedia"
    for pelicula in data:
        assert pelicula["categoria"] == "comedia"
