from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import Tablero, Tarjeta, Tarea, Comentario
from .forms import TareaForm, ComentarioForm, TarjetaForm
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
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        # Obtener el usuario logueado como propietario
        propietario = request.user

        # Crear el objeto Tablero
        nuevo_tablero = Tablero(
            nombre=nombre,
            descripcion=descripcion,
            propietario=propietario
        )

        # Guardar el tablero en la base de datos
        nuevo_tablero.save()

        # Redirigir a la página de inicio (home)
        return redirect('home')

    return render(request, 'creartablero.html')

@login_required
def tarjetaview(request, tablero_id):
    tablero = get_object_or_404(Tablero, id=tablero_id)

    # Verificar si el usuario actual es el creador del tablero
    if request.user != tablero.propietario:
        return redirect('home')  # O redirige a la página que desees si el usuario no es el creador

    tarjetas = Tarjeta.objects.filter(id_tablero=tablero_id)
    tareas = Tarea.objects.filter(id_tarjeta__in=tarjetas)
    comentarios = Comentario.objects.filter(tarjeta__in=tarjetas)

    tarea_form = TareaForm()
    comentario_form = ComentarioForm()
    tarjeta_form = TarjetaForm()

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
            tarjeta_form = TarjetaForm(request.POST)
            if tarjeta_form.is_valid():
                tarjeta = tarjeta_form.save(commit=False)
                tarjeta.id_tablero = tablero
                tarjeta.save()
        elif 'editar_tarea' in request.POST:
            tarea_form = TareaForm(request.POST)
            if tarea_form.is_valid():
                tarea_id = request.POST.get('tarea_id')
                tarea = get_object_or_404(Tarea, id=tarea_id)
                tarea.estado = tarea_form.cleaned_data['estado']
                tarea.save()

    return render(request, 'tarjetaview.html', {'tablero': tablero, 'tarjetas': tarjetas, 'tareas': tareas, 'comentarios': comentarios, 'tarea_form': tarea_form, 'comentario_form': comentario_form})


def profile(request):
    return render(request, 'profile.html')
