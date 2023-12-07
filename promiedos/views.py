from django.shortcuts import render, get_object_or_404, redirect
from .models import Liga, Equipo, Jugador, Partido
from .forms import CrearPartido, CheckWinner
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
    equipos = Equipo.objects.filter(league=liga).order_by('points')
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
    if request.method == 'GET':
        partido = get_object_or_404(Partido, pk=partido_id)
        form = CrearPartido(instance=partido)
        user = request.user
        local = partido.local
        visitante = partido.visitante
        jugadores_local = Jugador.objects.filter(
            equipo_jugador=local)
        jugadores_visitante = Jugador.objects.filter(
            equipo_jugador=visitante)

        return render(request, 'partido_detail.html', {'partido': partido, 'local': local, 'visitante': visitante, 'jugadores_local': jugadores_local, 'jugadores_visitante': jugadores_visitante, 'user': user, 'form': form, })
    elif request.method == 'POST':
        try:
            partido = get_object_or_404(Partido, pk=partido_id)
            form = CrearPartido(request.POST, instance=partido)
            form.save()
            return redirect('home')
        except ValueError:
            return render(request, 'partido_detail.html', {'partido': partido, 'local': local, 'visitante': visitante, 'jugadores_local': jugadores_local, 'jugadores_visitante': jugadores_visitante, 'user': user, 'form': form, 'error': 'An error has ocurred, please verify the data'})


def partido_finished(request, partido_id):
    if request.method == "POST":
        partido = get_object_or_404(Partido, pk=partido_id)
        partido.finished = True

        winner = CheckWinner(partido.goles_local, partido.goles_visitante)

        if winner == "local":
            print('equipo local', partido.local)
            print('antes', partido.local.points)
            partido.local.points += 3
            partido.local.points.save()
            print('despues', partido.local.points)
        elif winner == "visitante":
            print('equipo visitante', partido.visitante)
            print('antes', partido.visitante.points)
            partido.visitante.points += 3
            print('despues', partido.visitante.points)
        elif winner == "empate":
            partido.local.points += 1
            partido.visitante.points += 1
            print(partido.local.points)
            print(partido.visitante.points)
        else:
            print('Invalid Winner', winner)

        # partido.save()
        return redirect('home')
        # if partido.goles_local > partido.goles_visitante:
        #     partido.local.points += 3
        #     print("Local team won")
        # elif partido.goles_local < partido.goles_visitante:
        #     partido.visitante.points += 3
        #     print("visitante team won")
        # elif partido.goles_local == partido.goles_visitante:
        #     partido.local.points += 1
        #     partido.visitante.points += 1
        #     print("Empate")
