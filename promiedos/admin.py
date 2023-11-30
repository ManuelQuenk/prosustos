from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Liga),
admin.site.register(models.Equipo),
admin.site.register(models.Jugador),
admin.site.register(models.Partido),
