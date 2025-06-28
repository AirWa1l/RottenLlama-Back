from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Pelicula(models.Model):
    titulo = models.CharField(max_length=255)
    fecha = models.IntegerField()
    categoria = models.CharField(max_length=100)
    calificacion = models.DecimalField(max_digits=3, decimal_places=1,validators=[
            MinValueValidator(Decimal('0.0')),
            MaxValueValidator(Decimal('10.0'))
        ])
    director = models.CharField(max_length=100)
    imagen_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.titulo
