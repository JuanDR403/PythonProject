from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Tablero, Tarjeta, Tarea, Comentario, Historial
from .forms import TareaForm, ComentarioForm, TarjetaForm, TableroForm
from django.contrib.auth.decorators import permission_required


# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
@login_required
def home(request):
    # Obtener todos los tableros
    tableros = Tablero.objects.all()

    # Pasar los tableros al contexto
    context = {
        'tableros': tableros
    }

    return render(request, 'home.html', context)

def signout(request):
    logout(request)
    return redirect('/')

def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile') #profile
        else:
            msg = 'Error de Inicio de Sesion'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})

    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    

@login_required
def creartablero(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        tablero_form = TableroForm(request.POST)
        if tablero_form.is_valid():
            nuevo_tablero = tablero_form.save(commit=False)

            # Asignar al usuario logueado como propietario
            nuevo_tablero.propietario = request.user
            nuevo_tablero.save()

            # Agregar al propietario a la lista de usuarios permitidos
            nuevo_tablero.usuarios_permitidos.add(request.user)

            # Redirigir a la página de inicio (home)
            return redirect('home')
    else:
        tablero_form = TableroForm()

    return render(request, 'creartablero.html', {'tablero_form': tablero_form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Tablero, Tarjeta, Tarea, Comentario
from .forms import TareaForm, ComentarioForm, TarjetaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def tarjetaview(request, tablero_id):
    tablero = get_object_or_404(Tablero, id=tablero_id)

    # Inicializar tarjetas fuera del bloque if
    tarjetas = Tarjeta.objects.filter(id_tablero=tablero_id)
    tareas = Tarea.objects.filter(id_tarjeta__in=tarjetas)
    comentarios = Comentario.objects.filter(tarjeta__in=tarjetas)

    tarea_form = TareaForm()
    comentario_form = ComentarioForm()
    tarjeta_form = TarjetaForm(request.POST or None)

    # Verificar si el usuario actual está en la lista de usuarios permitidos
    if request.user not in tablero.usuarios_permitidos.all():
        # Si el usuario no tiene permiso, aún permitir ver las tarjetas
        return render(request, 'tarjetaview.html', {'tablero': tablero, 'tarjetas': tarjetas, 'tareas': tareas, 'comentarios': comentarios, 'tarea_form': tarea_form, 'comentario_form': comentario_form, 'tarjeta_form': tarjeta_form})    

    if request.method == 'POST':
        if 'agregar_tarea' in request.POST:
            tarea_form = TareaForm(request.POST)
            if tarea_form.is_valid():
                tarea = tarea_form.save(commit=False)
                tarea.id_tarjeta = get_object_or_404(Tarjeta, id=request.POST.get('tarjeta_id'))
                tarea.save()
        elif 'agregar_comentario' in request.POST:
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.tarjeta = get_object_or_404(Tarjeta, id=request.POST.get('tarjeta_id'))
                comentario.usuario = request.user  # Asigna el usuario actual
                comentario.save()
        elif 'agregar_tarjeta' in request.POST:
            # Verificar si el usuario actual es el propietario del tablero
            if request.user != tablero.propietario:
                return redirect('home')  # O redirige a la página que desees si el usuario no tiene permiso
            
            tarjeta_form = TarjetaForm(request.POST)
            if tarjeta_form.is_valid():
                tarjeta = tarjeta_form.save(commit=False)
                tarjeta.id_tablero = tablero
                tarjeta.save()
                
                # Redirige al usuario a la misma página para evitar reenviar el formulario al recargar
                return redirect('tarjetaview', tablero_id=tablero_id)
                
        elif 'editar_tarea' in request.POST:
            tarea_form = TareaForm(request.POST)
            if tarea_form.is_valid():
                tarea_id = request.POST.get('tarea_id')
                tarea = get_object_or_404(Tarea, id=tarea_id)
                tarea.estado = tarea_form.cleaned_data['estado']
                tarea.save()
        # Agregar usuarios permitidos al tablero
        elif 'agregar_usuarios_permitidos' in request.POST:
            usuarios_permitidos = request.POST.get('usuarios_permitidos')
            if usuarios_permitidos:
                usuarios_permitidos_list = usuarios_permitidos.split(',')
                for username in usuarios_permitidos_list:
                    usuario_permitido = User.objects.get(username=username.strip())
                    tablero.usuarios_permitidos.add(usuario_permitido)
                tablero.save()

    return render(request, 'tarjetaview.html', {'tablero': tablero, 'tarjetas': tarjetas, 'tareas': tareas, 'comentarios': comentarios, 'tarea_form': tarea_form, 'comentario_form': comentario_form, 'tarjeta_form': tarjeta_form})


def profile(request):
    return render(request, 'profile.html')


@login_required
def borrar_tablero(request, tablero_id):
    tablero = get_object_or_404(Tablero, id=tablero_id)

    # Verificar si el usuario actual es el propietario del tablero
    if request.user == tablero.propietario:
        tablero.delete()
    
    return redirect('home')

@login_required
def borrar_tarjeta(request, tarjeta_id):
    tarjeta = get_object_or_404(Tarjeta, id=tarjeta_id)

    # Verificar si el usuario actual es el propietario de la tarjeta o del tablero
    if request.user == tarjeta.id_tablero.propietario:
        tarjeta.delete()
    
    return redirect('tarjetaview', tablero_id=tarjeta.id_tablero.id)

def historial_view(request):
    historial = Historial.objects.all().order_by('-fecha')  # Obtener todas las entradas del historial
    return render(request, 'historial.html', {'historial': historial})