from django.shortcuts import render, get_object_or_404, redirect
from .models import Liga, Equipo, Jugador, Partido
from .forms import CrearPartido
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone

# Create your views here.


def home(request):
    partidos = Partido.objects.all()
    ligas = Liga.objects.all()
    equipos = Equipo.objects.all()
    return render(request, 'home.html', {'equipos': equipos, 'partidos': partidos, 'ligas': ligas, })


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Passwords do not match'
            })


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('home')


def liga_detail(request, liga_id):
    liga = get_object_or_404(Liga, pk=liga_id)
    equipos = Equipo.objects.filter(team_league=liga)
    return render(request, 'liga_detail.html', {'liga': liga, 'equipos': equipos, })


@login_required
@user_passes_test(lambda user: user.is_superuser)
def crear_partido(request):
    if request.method == 'GET':
        return render(request, 'crear_partido.html', {'form': CrearPartido, })
    else:
        try:
            form = CrearPartido(request.POST)
            if form.is_valid():
                nuevo_partido = form.save(commit=False)
                nuevo_partido.save()
                return redirect('home')
            else:
                return render(request, 'crear_partido.html', {'form': form, 'error': 'Check and provide valid data'})
        except ValueError:
            return render(request, 'crear_partido.html', {'form': CrearPartido, 'error': 'Check and provide valid data', })

def partido_detail(request, partido_id):
    return render(request, 'partido_detail.html')