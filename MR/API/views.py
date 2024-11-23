from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from API.models import Movie

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

def home(request):
    movies = Movie.objects.all()
    return render(request, 'Home.html', {'movies': movies})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def top_10_by_genrer(request):
    return render(request, 'Top_10_By_genrer.html')
@login_required
def top_10_by_user(request):
    return render(request, 'Top_10_User_Rate.html')