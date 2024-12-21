from django.contrib import admin
from django.urls import path
from API import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Páginas principales
    path('', views.home, name='home'),
    path('top10/', views.movie_list, name='top10'), 
    path('genres/', views.top_10_by_genrer, name='genres'), 
    path('advanced/', views.top_10_by_user, name='advanced'), 
    path('advanced/json/', views.get_top_10_by_user_json, name='get_top_10_by_user_json'),
    path('save-selected-movies/', views.save_selected_movies, name='save_selected_movies'),
    path('preparing/', views.preparing, name='preparing'),
    path('recommender/', views.recommender, name='recommender'),
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]