from django.contrib import admin
from django.urls import path
from API import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns = [
    path('', views.movie_list, name='movie_list'),  # Accede a la vista movie_list
]