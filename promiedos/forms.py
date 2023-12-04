from django import forms
from .models import Partido


class CrearPartido(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ['date', 'local', 'visitante',
                  'goles_local', 'goles_visitante', 'finished',]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%d-%mT%H:%M'),
        }
