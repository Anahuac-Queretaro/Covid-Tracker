from datetime import datetime
import json
import pytz

from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings


from .forms import (
    InternalRegisterAttendanceForm,
    ExternalRegisterAttendanceForm,
    AlertForm
)

from .tasks import alert_covid


class RegisterView(TemplateView):
    form_class = None

    def get(self, request):
        room = request.GET.get('room')
        current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M")

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
    template_name = 'internal-register.html'
    form_class = InternalRegisterAttendanceForm


class ExternalRegisterView(RegisterView):
    template_name = 'external-register.html'
    form_class = ExternalRegisterAttendanceForm

class AlertView(TemplateView):
    template_name = 'alert.html'

    def get(self, request):
        form = AlertForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AlertForm(request.POST)
        if form.is_valid():
            form_fields = form.cleaned_data
            self.alert_covid(
                form_fields['email'],
                form_fields['exposure_date']
            )
            messages.success(request, 'Alerta lanzada correctamente. Se están notificando a las personas con las que tuviste contacto')
        else:
            string_error = form.errors.as_json(escape_html=False)
            dict_error = json.loads(string_error)
            for error in form.errors:
                for err in dict_error[error]:
                    messages.error(request, err['message'])

        return render(request, self.template_name, {'form': form})

    def alert_covid(self, suspect_email, exposure_date):
        """Search all the people that were exposed and
        informed them via email using celery tasks"""
        current_timezone = pytz.timezone(settings.TIME_ZONE)
        exposure_date_without_tz = datetime.strptime(
            f'{exposure_date} 00:00', '%Y-%m-%d %H:%M'
        )
        exposure_date_with_tz = exposure_date_without_tz.replace(
            tzinfo=current_timezone
        )
        #exposed_people = alert_covid.delay(suspect_email, exposure_date_with_tz)
        alert_covid.delay(suspect_email, exposure_date_with_tz)
