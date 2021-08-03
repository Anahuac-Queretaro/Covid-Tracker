from django.db import models


class Building(models.Model):
    "Building model"
    name = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_building_name_constraint'),
        ]

    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    "Room model"
    name = models.CharField(max_length=255)
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'building'], name='unique_room_name_per_building_constraint'),
        ]

    def __str__(self):
        return f'{self.building} - {self.name}'
