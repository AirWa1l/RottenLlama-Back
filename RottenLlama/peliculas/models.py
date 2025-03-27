from django.db import models

class Pelicula(models.Model):
    titulo = models.CharField(max_length=255)
    fecha = models.IntegerField()
    categoria = models.CharField(max_length=100)
    calificacion = models.DecimalField(max_digits=3, decimal_places=1)
    

    def __str__(self):
        return self.titulo
