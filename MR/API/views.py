from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from API.models import Movie, Genre, MovieRating
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
#Procesos de sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
#librerias extras y de preprocesamiento de texto
import numpy as np
from numpy import array
import threading
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

def home(request):
    movies = Movie.objects.all().order_by('?')[:12]
    return render(request, 'Home.html', {'movies': movies})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        # Depuración completa de los datos POST
        print("Datos POST completos:", dict(request.POST))

        # Lógica de inicio de sesión
        if request.POST.get('form_type') == 'login':
            email = request.POST.get('login_email')
            password = request.POST.get('login_password')

            print(f"Intento de login - Email: {email}")
            
            # Intentar encontrar el usuario por email
            try:
                user_obj = User.objects.filter(email=email).first()
                username = user_obj.username
            
            except Exception as e:
                print(f"Error al encontrar usuario: {str(e)}")
                messages.error(request, f'Error al encontrar usuario: {str(e)}')
                return render(request, 'login.html')

            # Autenticar
            user = authenticate(username=username, password=password)

            if user is not None:
                print(f"Autenticación exitosa para {email}")
                login(request, user)
                messages.success(request, '¡Inicio de sesión exitoso!')
                return redirect('home')
            else:
                print(f"Autenticación fallida para {email}")
                messages.error(request, 'Correo electrónico o contraseña incorrectos')
                return render(request, 'login.html')

        # Lógica de registro de nuevo usuario
        elif request.POST.get('form_type') == 'signup':
            username = request.POST.get('username')
            name = request.POST.get('signup_name')
            email = request.POST.get('signup_email')
            password = request.POST.get('signup_password')

            print(f"Intento de registro - Nombre: {name}, Email: {email}")

            # Verificar si el usuario ya existe
            if User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado')
                return render(request, 'login.html')

            try:
                # Crear usuario
                user = User.objects.create_user(
                    username=username, 
                    email=email,
                    password=password,
                    first_name=name,
                    is_staff=False,
                    is_superuser=False
                )

                # Autenticar e iniciar sesión
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, '¡Registro exitoso!')
                    return redirect('home')
                else:
                    print("Error: No se pudo autenticar al usuario recién creado")
                    messages.success(request, 'Se creo la cuenta')
                    return render(request, 'login.html')  # Agregar este return

            except Exception as e:
                # Depuración de errores
                print(f"Error en la creación de usuario: {str(e)}")
                messages.error(request, f'Error en el registro: {str(e)}')
                return render(request, 'login.html')  # Agregar este return
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def top_10_by_genrer(request):
    genres = Genre.objects.all()
    selected_genre = request.GET.get('genre', None)

    # Depuración: imprime el género seleccionado
    print(f"Género seleccionado: {selected_genre}")

    if selected_genre:
        top_movies = Movie.objects.filter(moviegenre__genre__name=selected_genre).order_by('-vote_average')[:10]
    else:
        top_movies = Movie.objects.all().order_by('-vote_average')[:10]

    context = {
        'genres': genres,
        'selected_genre': selected_genre,
        'top_movies': top_movies
    }

    # Manejo de solicitudes AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = [{
            'imagen': movie.imagen,
            'title': movie.title,
            'director': movie.director.director_name if movie.director else 'Sin director',
            'vote_average': movie.vote_average,
            'sipnosis': movie.sipnosis
        } for movie in top_movies]

        # Depuración: imprime los datos que se enviarán
        print("Datos JSON enviados:", data)

        return JsonResponse(data, safe=False)

    return render(request, 'Top_10_By_genrer.html', context)

@login_required
def top_10_by_user(request):
    global resultado
    resultado = None
    user_id = request.user.id
    rated_movies = MovieRating.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
    movies = Movie.objects.exclude(id__in=rated_movies).order_by('?')[:10]
    return render(request, 'Top_10_User_Rate.html', {'movies': movies})

def get_top_10_by_user_json(request):
    user = request.user
    user_ratings = MovieRating.objects.filter(user_id=user.id).values_list('movie_id', flat=True)
    movies = Movie.objects.exclude(id__in=user_ratings).order_by('?')

    page = request.GET.get('page', 1)
    paginator = Paginator(movies, 12)

    try:
        movies_page = paginator.page(page)
    except PageNotAnInteger:
        movies_page = paginator.page(1)
    except EmptyPage:
        movies_page = paginator.page(paginator.num_pages)

    data = [{'id': movie.id, 'title': movie.title, 'imagen': movie.imagen} for movie in movies_page]

    return JsonResponse(data, safe=False)

@require_http_methods(['POST'])
def save_selected_movies(request):
    print("Se recibió una solicitud POST")
    movies = request.POST.getlist('movies[]')
    ratings = request.POST.getlist('ratings[]')
    print("Películas:", movies)
    print("Calificaciones:", ratings)

    try:
        user = request.user
        print("Usuario:", user)
        for i, movie_id in enumerate(movies):
            movie = Movie.objects.get(id=movie_id)
            rating = float(ratings[i])
            print("Película:", movie)
            print("Calificación:", rating)
            try:
                rating_obj = MovieRating.objects.get(user_id=user, movie_id=movie)
                print("Se encontró una calificación existente")
                rating_obj.rating = rating
                rating_obj.save()
                print("Se actualizó la calificación")
            except MovieRating.DoesNotExist:
                print("No se encontró una calificación existente")
                MovieRating.objects.create(user_id=user, movie_id=movie, rating=rating)
                print("Se creó una nueva calificación")

        return JsonResponse({'message': 'Películas guardadas correctamente'})
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Película no encontrada'}, status=404)
    
def preparing(request):
    user_id = request.user.id
    thread = threading.Thread(target=obtener_recomendaciones_avanzadas, args=(user_id,))
    thread.start()
    return render(request, 'Preparing.html')

resultado = None

def obtener_recomendaciones_avanzadas(user_id):
    # Obtener las calificaciones del usuario
    user_ratings = MovieRating.objects.filter(user_id=user_id).values_list('movie_id', 'rating')

    # Obtener las sinopsis de las películas
    sinopsis = Movie.objects.all().values_list('sipnosis', flat=True)

    # Preprocesar las sinopsis
    sinopsis_preprocesadas = [preprocesar_texto(sinopsis_) for sinopsis_ in sinopsis]

    # Crear una matriz TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sinopsis_preprocesadas)

    # Normalizar la matriz TF-IDF
    tfidf_matrix_normalizado = normalize(tfidf_matrix)

    # Crear un vector de características del usuario basado en sus calificaciones
    user_profile = np.zeros(tfidf_matrix_normalizado.shape[1])
    for movie_id, rating in user_ratings:
        movie_index = list(Movie.objects.all().values_list('id', flat=True)).index(movie_id)
        user_profile += tfidf_matrix_normalizado[movie_index].toarray()[0] * float(rating)

    # Calcular similitud coseno entre el perfil del usuario y todas las películas
    cosine_similarities = cosine_similarity(user_profile.reshape(1, -1), tfidf_matrix_normalizado)[0]

    # Crear un diccionario para almacenar la mejor similitud para cada película
    best_similarities = {}

    # Iterar sobre todas las películas y sus similitudes
    for idx, similarity in enumerate(cosine_similarities):
        movie_id = list(Movie.objects.all().values_list('id', flat=True))[idx]
        movie_title = Movie.objects.get(id=movie_id).title
        if movie_id not in [mr[0] for mr in user_ratings]:
            if movie_title not in best_similarities or similarity > best_similarities[movie_title][1]:
                best_similarities[movie_title] = (Movie.objects.get(id=movie_id).vote_average, similarity)

    # Convertir el diccionario a una lista de tuplas y ordenar por similitud
    recommendations = [(title, rating, similarity) for title, (rating, similarity) in best_similarities.items()]
    recommendations.sort(key=lambda x: x[2], reverse=True)

    # Tomar las top 10 recomendaciones
    top_recommendations = recommendations[:10]

    # Obtener los IDs de las películas recomendadas
    movie_ids = [Movie.objects.get(title=recommendation[0]).id for recommendation in top_recommendations]

    # Filtrar las películas recomendadas utilizando sus IDs
    movies = Movie.objects.filter(id__in=movie_ids)

    global resultado
    resultado = movies

#Preprocesamiento del texto
def preprocesar_texto(texto):
    # Tokenizar el texto
    tokens = word_tokenize(texto)
    
    # Eliminar stopwords
    stopwords_ = set(stopwords.words('spanish'))
    tokens = [token for token in tokens if token not in stopwords_]
    
    # Stemming
    stemmer = SnowballStemmer('spanish')
    tokens = [stemmer.stem(token) for token in tokens]
    
    # Unir los tokens en un solo string
    texto_preprocesado = ' '.join(tokens)
    
    return texto_preprocesado


def recommender(request):
    global resultado
    print(resultado)
    return render(request, 'Recommender.html', {'movies': resultado})
