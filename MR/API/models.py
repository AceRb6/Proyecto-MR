from django.db import models
from django.contrib.auth.models import User 
class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'directors'  # Nombre de la tabla sin prefijo


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'genres'  # Nombre de la tabla sin prefijo


class Movie(models.Model):
    title = models.CharField(max_length=255)
    vote_average = models.FloatField()
    keywords = models.TextField()
    cast = models.TextField(db_column='cast_')
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    sipnosis = models.TextField()
    imagen = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movies'  # Nombre de la tabla sin prefijo


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_genres'  # Nombre de la tabla sin prefijo

class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Relación con la película
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # Calificación, por ejemplo, de 1 a 10 con un decimal
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora en que se registró la calificación

    def __str__(self):
        return f'{self.user.username} - {self.movie.title} - {self.rating}'

    class Meta:
        db_table = 'movie_ratings'  # Nombre de la tabla en la base de datos
        unique_together = ('user', 'movie')  # Evita duplicar calificaciones para un usuario y una película
