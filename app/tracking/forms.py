from django import forms
from core.models import Room


class RegisterAttendanceForm(forms.Form):
    room = forms.ModelChoiceField(
        Room.objects,
        empty_label=None,
        label='Salón',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    entry_datetime = forms.DateTimeField(
        label='Fecha y hora de ingreso',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    email = forms.EmailField(
        label='Correo institucional',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    exit_datetime = forms.DateTimeField(
        label='Fecha y hora aproximada de salida (¿a qué hora estimas salir?)',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
