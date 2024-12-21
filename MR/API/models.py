from django.db import models
from django.contrib.auth.models import User 
class Director(models.Model):
    director_name = models.CharField(max_length=255)

    def __str__(self):
        return self.director_name

    class Meta:
        db_table = 'directors'  # Nombre de la tabla sin prefijo


class Genre(models.Model):
    name = models.CharField(max_length=255, db_column='genre_name')

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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE,default=None)
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        db_table = 'movie_ratings'  # Nombre de la tabla sin prefijo
        unique_together = ('user_id', 'movie_id')