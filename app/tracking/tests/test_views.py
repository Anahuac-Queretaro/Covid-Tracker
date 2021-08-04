from http import HTTPStatus
from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware

from core.models import Building, Room, AttendanceRecord


class ViewsTests(TestCase):
    def test_display_form(self):
        """Test get the internal attendance html"""
        response = self.client.get(reverse('tracking:internal-register'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response,
            '<h1>Registro de Entrada Comunidad Anáhuac</h1>',
            html=True
        )

    def test_post_internal_attendance_success(self):
        """Test the post of internal attendance is successfull"""
        building_name = 'Building 1'
        room_name = 'Room 1'

        building = Building.objects.create(
            name=building_name
        )
        room = Room.objects.create(
            name=room_name,
            building=building
        )
        post_data = {'room': room.id,
                     'entry_datetime': '2021-08-04T10:00',
                     'attendee_email': 'student@anahuac.mx',
                     'exit_datetime': '2021-08-04T11:30'}
        response = self.client.post(
            reverse('tracking:internal-register'),
            post_data
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(response.context['messages'])
        success_message = str(messages[0])
        self.assertEqual(success_message, 'Registro realizado exitosamente')

    def test_post_internal_attendance_fail_invalid_room(self):
        """Test the post of internal attendance fail because invalid room id"""

        post_data = {'room': 4,
                     'entry_datetime': '2021-08-04T10:00',
                     'attendee_email': 'student@anahuac.mx',
                     'exit_datetime': '2021-08-04T11:30'}
        response = self.client.post(
            reverse('tracking:internal-register'),
            post_data
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(response.context['messages'])
        error_message = str(messages[0])
        self.assertEqual(error_message, 'El salón seleccionado no es válido')

    def test_post_internal_attendance_fail_invalid_email(self):
        """Test the post of internal attendance fail because invalid email"""
        building_name = 'Building 1'
        room_name = 'Room 1'

        building = Building.objects.create(
            name=building_name
        )
        room = Room.objects.create(
            name=room_name,
            building=building
        )

        post_data = {'room': room.id,
                     'entry_datetime': '2021-08-04T10:00',
                     'attendee_email': 'student@external.mx',
                     'exit_datetime': '2021-08-04T11:30'}
        response = self.client.post(
            reverse('tracking:internal-register'),
            post_data
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(response.context['messages'])
        error_message = str(messages[0])
        invalid_email_error_msg = ('El correo electrónico no es válido. Si no cuentas con un correo de la Anáhuac, '
                                   'usa el registro para invitados')
        self.assertEqual(error_message, invalid_email_error_msg)

    def test_post_internal_attendance_fail_already_registered_upper_limit(self):
        """Test the post of internal attendance fail because the
        email was already registered in the same spawn of time.
        The start date is inside another"""
        building_name = 'Building 1'
        room_name = 'Room 1'

        building = Building.objects.create(
            name=building_name
        )
        room = Room.objects.create(
            name=room_name,
            building=building
        )

        AttendanceRecord.objects.create(
            room=room,
            entry_datetime=make_aware(datetime.strptime('2021-08-03T20:30', '%Y-%m-%dT%H:%M')),
            exit_datetime=make_aware(datetime.strptime('2021-08-03T22:00', '%Y-%m-%dT%H:%M')),
            attendee_email='student@anahuac.mx'
        )

        post_data = {'room': room.id,
                     'entry_datetime': '2021-08-03T21:00',
                     'attendee_email': 'student@anahuac.mx',
                     'exit_datetime': '2021-08-03T22:30'}
        response = self.client.post(
            reverse('tracking:internal-register'),
            post_data
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(response.context['messages'])
        error_message = str(messages[0])
        invalid_date_error_msg = ('Ya existe un registro que coincide con ese lapso de tiempo: '
                                  'Building 1 - Room 1 - 2021-08-03 20:30 - 2021-08-03 22:00')
        self.assertEqual(error_message, invalid_date_error_msg)

    def test_post_internal_attendance_fail_already_registered_under_limit(self):
        """Test the post of internal attendance fail because the
        email was already registered in the same spawn of time.
        The end date is inside another"""
        building_name = 'Building 1'
        room_name = 'Room 1'

        building = Building.objects.create(
            name=building_name
        )
        room = Room.objects.create(
            name=room_name,
            building=building
        )

        AttendanceRecord.objects.create(
            room=room,
            entry_datetime=make_aware(datetime.strptime('2021-08-03T20:30', '%Y-%m-%dT%H:%M')),
            exit_datetime=make_aware(datetime.strptime('2021-08-03T22:00', '%Y-%m-%dT%H:%M')),
            attendee_email='student@anahuac.mx'
        )

        post_data = {'room': room.id,
                     'entry_datetime': '2021-08-03T19:00',
                     'attendee_email': 'student@anahuac.mx',
                     'exit_datetime': '2021-08-03T21:00'}
        response = self.client.post(
            reverse('tracking:internal-register'),
            post_data
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(response.context['messages'])
        error_message = str(messages[0])
        invalid_date_error_msg = ('Ya existe un registro que coincide con ese lapso de tiempo: '
                                  'Building 1 - Room 1 - 2021-08-03 20:30 - 2021-08-03 22:00')
        self.assertEqual(error_message, invalid_date_error_msg)

    def test_post_internal_attendance_fail_already_registered_inside(self):
        """Test the post of internal attendance fail because the
        email was already registered in the same spawn of time.
        The date has another one inside"""
        building_name = 'Building 1'
        room_name = 'Room 1'

        building = Building.objects.create(
            name=building_name
        )
        room = Room.objects.create(
            name=room_name,
            building=building
        )

        AttendanceRecord.objects.create(
            room=room,
            entry_datetime=make_aware(datetime.strptime('2021-08-03T20:30', '%Y-%m-%dT%H:%M')),
            exit_datetime=make_aware(datetime.strptime('2021-08-03T22:00', '%Y-%m-%dT%H:%M')),
            attendee_email='student@anahuac.mx'
        )

        post_data = {'room': room.id,
                     'entry_datetime': '2021-08-03T19:00',
                     'attendee_email': 'student@anahuac.mx',
                     'exit_datetime': '2021-08-03T23:00'}
        response = self.client.post(
            reverse('tracking:internal-register'),
            post_data
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(response.context['messages'])
        error_message = str(messages[0])
        invalid_date_error_msg = ('Ya existe un registro que coincide con ese lapso de tiempo: '
                                  'Building 1 - Room 1 - 2021-08-03 20:30 - 2021-08-03 22:00')
        self.assertEqual(error_message, invalid_date_error_msg)

    def test_post_internal_attendance_fail_invalid_date_range(self):
        """Test the post of internal attendance fail because
        invalid date range. Exit is smaller than entry"""
        building_name = 'Building 1'
        room_name = 'Room 1'

        building = Building.objects.create(
            name=building_name
        )
        room = Room.objects.create(
            name=room_name,
            building=building
        )
        post_data = {'room': room.id,
                     'entry_datetime': '2021-08-03T19:00',
                     'attendee_email': 'student@anahuac.mx',
                     'exit_datetime': '2021-08-03T18:00'}
        response = self.client.post(
            reverse('tracking:internal-register'),
            post_data
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(response.context['messages'])
        error_message = str(messages[0])
        invalid_date_error_msg = ('La fecha de salida no puede ser menor o igual que la fecha de entrada')
        self.assertEqual(error_message, invalid_date_error_msg)

    def test_post_external_attendance_successfull(self):
        """Test the post of external attendace is sucessfull"""
        building_name = 'Building 1'
        room_name = 'Room 1'

        building = Building.objects.create(
            name=building_name
        )
        room = Room.objects.create(
            name=room_name,
            building=building
        )
        post_data = {'room': room.id,
                     'entry_datetime': '2021-08-03T19:00',
                     'attendee_email': 'student@external.mx',
                     'exit_datetime': '2021-08-03T20:00'}
        response = self.client.post(
            reverse('tracking:external-register'),
            post_data
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(response.context['messages'])
        success_message = str(messages[0])
        self.assertEqual(success_message, 'Registro realizado exitosamente')
