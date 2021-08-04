from datetime import datetime

from django.test import TestCase
from django.utils.timezone import make_aware

from core import models


class ModelTests(TestCase):
    def test_create_building_successfull(self):
        """Test if a new building is created"""
        name = 'Building 1'

        models.Building.objects.create(
            name=name
        )

        buildings = models.Building.objects.filter(name=name)
        self.assertEqual(buildings.count(), 1)

    def test_building_str(self):
        """Test if the str for the building is set correctly"""
        name = 'Building 1'

        building = models.Building.objects.create(
            name=name
        )

        self.assertEqual(str(building), name)

    def test_create_room_successfull(self):
        """Test if a new room is created"""
        building = models.Building.objects.create(
            name='Building 1'
        )
        name = 'Room 1'

        models.Room.objects.create(
            name=name,
            building=building
        )

        rooms = models.Room.objects.filter(name=name, building=building)
        self.assertEqual(rooms.count(), 1)

    def test_room_str(self):
        """Test if the str of the room is right"""
        building = models.Building.objects.create(
            name='Building 1'
        )
        name = 'Room 1'

        room = models.Room.objects.create(
            name=name,
            building=building
        )

        self.assertEqual(str(room), f'{building.name} - {room.name}')

    def test_create_attendance_record_successfull(self):
        """Test if a new attendance record is created"""
        building = models.Building.objects.create(
            name='Building 1'
        )
        name = 'Room 1'

        room = models.Room.objects.create(
            name=name,
            building=building
        )

        models.AttendanceRecord.objects.create(
            room=room,
            entry_datetime=make_aware(datetime.strptime('2021-08-03T20:30', '%Y-%m-%dT%H:%M')),
            exit_datetime=make_aware(datetime.strptime('2021-08-03T22:00', '%Y-%m-%dT%H:%M')),
            attendee_email='test@anahuac.mx'
        )
        attendance_records = models.AttendanceRecord.objects.all()
        self.assertEqual(attendance_records.count(), 1)

    def test_attendace_record_str(self):
        """Test string for attendance record"""
        building = models.Building.objects.create(
            name='Building 1'
        )
        name = 'Room 1'

        room = models.Room.objects.create(
            name=name,
            building=building
        )

        record = models.AttendanceRecord.objects.create(
            room=room,
            entry_datetime=make_aware(datetime.strptime('2021-08-03T20:30', '%Y-%m-%dT%H:%M')),
            exit_datetime=make_aware(datetime.strptime('2021-08-03T22:00', '%Y-%m-%dT%H:%M')),
            attendee_email='test@anahuac.mx'
        )
        attendance_record_str = 'test@anahuac.mx - Building 1 - Room 1 - 2021-08-03 20:30:00-05:00 - 2021-08-03 22:00:00-05:00'
        self.assertEqual(str(record), attendance_record_str)
