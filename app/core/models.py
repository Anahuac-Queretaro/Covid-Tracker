from django.db import models


class Building(models.Model):
    """Building model"""
    name = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_building_name_constraint'),
        ]

    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    """Room model"""
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


class AttendanceRecord(models.Model):
    """Attendance model"""
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )
    entry_datetime = models.DateTimeField()
    exit_datetime = models.DateTimeField()
    attendee_email = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['attendee_email'], name='attendee_email_index'),
            models.Index(fields=['entry_datetime', 'exit_datetime'], name='entry_and_exit_attendee_index'),
        ]

    def __str__(self):
        return f'{self.attendee_email} - {self.room} - {self.entry_datetime} - {self.exit_datetime}'
