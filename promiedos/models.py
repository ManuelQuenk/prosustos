from django.db import models

# Create your models here.


class Liga(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Equipo(models.Model):
    team_name = models.CharField(max_length=200)
    team_league = models.ForeignKey(Liga, on_delete=models.CASCADE)
    team_points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.team_name}'


class Jugador(models.Model):
    ROLE_CHOICES = [
        ('ARQ', 1),
        ('DEF', 2),
        ('MD', 3),
        ('DC', 4),
    ]

    player_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    role = models.CharField(max_length=3, choices=ROLE_CHOICES)
    equipo_jugador = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.player_name + ' - ' + self.equipo_jugador.team_name


class Partido(models.Model):
    date = models.DateTimeField()
    local = models.ForeignKey(
        Equipo, related_name='partidos_local', on_delete=models.CASCADE)
    visitante = models.ForeignKey(
        Equipo, related_name='partidos_visitante', on_delete=models.CASCADE)
    goles_local = models.IntegerField(default=0)
    goles_visitante = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    def __str__(self):
        formatted_date = self.date.strftime("%d-%m %H:%M")
        return f'{formatted_date} | {self.local.team_name} {self.goles_local} - {self.goles_visitante} {self.visitante.team_name} | testing: L= {self.local.team_points} v= {self.visitante.team_points}'
