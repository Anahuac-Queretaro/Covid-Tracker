import datetime
import json

from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages

from .forms import InternalRegisterAttendanceForm, ExternalRegisterAttendanceForm


class RegisterView(TemplateView):
    form_class = None

    def get(self, request):
        room = request.GET.get('room')
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

        initial = {'room': room, 'entry_datetime': current_datetime}
        form = self.form_class(initial=initial)

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, 'Registro realizado exitosamente')
            form.save()
        else:
            string_error = form.errors.as_json(escape_html=False)
            dict_error = json.loads(string_error)
            for error in form.errors:
                for err in dict_error[error]:
                    messages.error(request, err['message'])

        return render(request, self.template_name, {'form': form})


class InternalRegisterView(RegisterView):
    template_name = "internal-register.html"
    form_class = InternalRegisterAttendanceForm


class ExternalRegisterView(RegisterView):
    template_name = "external-register.html"
    form_class = ExternalRegisterAttendanceForm
