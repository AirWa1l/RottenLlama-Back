from django.urls import path
from .views import (
    PeliculaListView,
    PeliculasPopularesView,
    PeliculaPorCategoriaView,
    PeliculasRecientesView,
    PeliculaDetailView
)

urlpatterns = [
    # Listado general
    path('peliculas/', PeliculaListView.as_view(), name='peliculas-list'),
    
    # Endpoints especiales
    path('peliculas/categoria/', PeliculaPorCategoriaView.as_view(), name='peliculas-por-categoria'),
    path('peliculas/populares/', PeliculasPopularesView.as_view(), name='peliculas-populares'),
    path('peliculas/recientes/', PeliculasRecientesView.as_view(), name='peliculas-recientes'),
    
    # Operaciones CRUD individuales
    path('peliculas/<int:pk>/', PeliculaDetailView.as_view(), name='pelicula-detail'),
]