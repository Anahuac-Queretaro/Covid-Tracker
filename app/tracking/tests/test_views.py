from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


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
        post_data = {'room': 1,
                     'entry_datetime': '2021-08-04T10:00',
                     'email': 'student@anahuac.mx',
                     'exit_datetime': '2021-08-04T11:30'}
        response = self.client.post(
            reverse('tracking:internal-register'),
            post_data
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(response.context['messages'])
        print(messages)
