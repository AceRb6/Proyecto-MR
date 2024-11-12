from django.contrib import admin
from django.urls import path
from API import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns = [
    path('', views.movie_list, name='movie_list'),  # Accede a la vista movie_list
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])