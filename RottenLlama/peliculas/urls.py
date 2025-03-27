from django.urls import path
from .views import PeliculaListView, PeliculasPopularesView,PeliculaPorCategoriaView

urlpatterns = [
    path('peliculas/', PeliculaListView.as_view(), name='peliculas-list'),
    path('peliculas/categoria/', PeliculaPorCategoriaView.as_view(), name='peliculas-por-categoria'),
    path('peliculas/populares/', PeliculasPopularesView.as_view(), name='peliculas-populares'),
]

