from django.shortcuts import render
from API.models import Movie

def movie_list(request):
    movies = Movie.objects.all()  # Obtiene todas las películas de la base de datos
    return render(request, 'movie_list.html', {'movies': movies})  # Pasa las películas al template