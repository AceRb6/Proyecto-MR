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
    path('top10/', views.movie_list, name='top10'),  # Cambiado para coincidir con el template
    path('genres/',  views.top_10_by_genrer, name='genres'),  # Cambiado para coincidir con el template
    path('advanced/', views.top_10_by_user, name='advanced'),  # Nueva ruta para recomendación avanzada
    
    # Autenticación
    path('login/', views.login_view, name='login'),  # Cambiado a login_view para evitar conflicto
    #path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]

# Configuración de archivos estáticos
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)