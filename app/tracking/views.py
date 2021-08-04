import datetime

from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages

from .forms import RegisterAttendanceForm


class RegisterView(TemplateView):
    form_class = RegisterAttendanceForm

    def get(self, request):
        room = request.GET.get('room')
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

        initial = {'room': room, 'entry_datetime': current_datetime}
        form = self.form_class(initial=initial)

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterAttendanceForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Registro realizado exitosamente')
        else:
            messages.error(request, 'Datos incorrectos')

        return render(request, self.template_name, {'form': form})


class InternalRegisterView(RegisterView):
    template_name = "internal-register.html"
