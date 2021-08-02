from django.test import TestCase

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
