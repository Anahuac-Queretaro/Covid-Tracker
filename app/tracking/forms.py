import pytz

from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms.widgets import DateTimeInput, EmailInput, Select
from django.db.models import Q
from django.conf import settings

from core.models import AttendanceRecord


class RegisterAttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'
        widgets = {
            'room': Select(attrs={'class': 'form-control'}),
            'entry_datetime': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'attendee_email': EmailInput(attrs={'class': 'form-control'}),
            'exit_datetime': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
        }
        error_messages = {
            'room': {
                'invalid_choice': _('El salón seleccionado no es válido')
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        entry_datetime = cleaned_data.get('entry_datetime')
        exit_datetime = cleaned_data.get('exit_datetime')
        attendee_email = cleaned_data.get('attendee_email')

        if entry_datetime >= exit_datetime:
            self.add_error(
                'entry_datetime',
                'La fecha de salida no puede ser menor o igual que la fecha de entrada'
            )

        start_date_between_another = Q(
            entry_datetime__lte=entry_datetime,
            exit_datetime__gt=entry_datetime
        )
        end_date_between_another = Q(
            entry_datetime__lt=exit_datetime,
            exit_datetime__gte=exit_datetime
        )
        date_inside_antoher = Q(
            entry_datetime__gte=entry_datetime,
            exit_datetime__lte=exit_datetime
        )
        same_attendee = Q(
            attendee_email=attendee_email
        )

        attendance_record = AttendanceRecord.objects.filter(
            same_attendee
            & (
                start_date_between_another
                | end_date_between_another
                | date_inside_antoher
            )
        )

        if attendance_record.count() != 0:
            first_attendance_record = attendance_record[0]

            current_timezone = pytz.timezone(settings.TIME_ZONE)
            date_format = '%Y-%m-%d %H:%M'
            entry_datetime_without_tz = first_attendance_record.entry_datetime
            entry_datetime_with_tz = entry_datetime_without_tz.astimezone(current_timezone).strftime(date_format)
            exit_datetime_without_tz = first_attendance_record.exit_datetime
            exit_datetime_with_tz = exit_datetime_without_tz.astimezone(current_timezone).strftime(date_format)

            attendance_record_info = (f'{first_attendance_record.room} - '
                                      f'{entry_datetime_with_tz} - {exit_datetime_with_tz}')
            self.add_error(
                'entry_datetime',
                f'Ya existe un registro que coincide con ese lapso de tiempo: {attendance_record_info}'
            )

        return cleaned_data


class InternalRegisterAttendanceForm(RegisterAttendanceForm):
    class Meta(RegisterAttendanceForm.Meta):
        labels = {
            'room': _('Salón'),
            'entry_datetime': _('Hora de entrada'),
            'attendee_email': _('Correo Institucional'),
            'exit_datetime': _('Hora de salida aproximada (¿a qué hora estimas salir?)')
        }

    def clean(self):
        cleaned_data = super().clean()
        attendee_email = cleaned_data.get('attendee_email')

        email_domain = attendee_email.split('@')[1]
        if email_domain != 'anahuac.mx':
            self.add_error(
                'attendee_email',
                'El correo electrónico no es válido. Si no cuentas con un correo de la Anáhuac, usa el registro para invitados'
            )


class ExternalRegisterAttendanceForm(RegisterAttendanceForm):
    class Meta(RegisterAttendanceForm.Meta):
        labels = {
            'room': _('Salón'),
            'entry_datetime': _('Hora de entrada'),
            'attendee_email': _('Correo electrónico'),
            'exit_datetime': _('Hora de salida aproximada (¿a qué hora estimas salir?')
        }
