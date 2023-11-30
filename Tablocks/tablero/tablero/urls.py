# tablero/urls.py

from django.contrib import admin
from django.urls import path
from libreria import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),  # Corregí el nombre de la vista a 'signout'.
    path('profile/', views.profile, name='profile'),
    path('creartablero/', views.creartablero, name='creartablero'),
    path('tarjetaview/<int:tablero_id>/', views.tarjetaview, name='tarjetaview'),
    path('agregar_tarea/<int:tarjeta_id>/', views.tarjetaview, name='agregar_tarea'),
    path('agregar_comentario/<int:tarjeta_id>/', views.tarjetaview, name='agregar_comentario'),
]

# Añade estas líneas para servir archivos estáticos durante el desarrollo.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
