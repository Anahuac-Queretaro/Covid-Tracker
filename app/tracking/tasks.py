from celery import shared_task

from django.db.models import Q
from django.core.mail import send_mail

from core.models import AttendanceRecord


@shared_task
def alert_covid(suspect_email, exposure_date):
    contaminated_rooms = get_rooms_and_dates(
            suspect_email,
            exposure_date
        )

    exposed_attendees = get_exposed_attendees(
        contaminated_rooms,
        exposure_date,
        suspect_email
    )

    emails = get_email_list(exposed_attendees)
    send_alert_email(emails)
    return 'Alert email sent'

@shared_task
def send_alert_email(emails):
    send_mail(
        'Alerta Covid',
        'Alguien con quien tuviste contacto lanzó la aleta COVID-19.',
        'from@example.com',
        emails,
    )

@shared_task
def get_email_list(exposed_attendees):
    emails = set()
    for record in exposed_attendees:
        emails.add(record.attendee_email)
    
    return emails

@shared_task
def get_exposed_attendees(contaminated_rooms, 
        exposure_date, suspect_email):
    """Get all the possible exposed attendees info"""
    registries_to_filter = AttendanceRecord.objects.filter(
        ~Q(attendee_email=suspect_email),
        entry_datetime__gte=exposure_date
    )

    exposed_attendees = list()
    for room in contaminated_rooms:
        entry_between_date_filter = Q(
            entry_datetime__lte=room['entry_datetime'],
            exit_datetime__gt=room['entry_datetime']
        )
        exit_between_date_filter = Q(
            entry_datetime__lt=room['exit_datetime'],
            exit_datetime__gte=room['exit_datetime']
        )
        same_room_filter = Q(
            room=room['room']
        )
        exposed_people = registries_to_filter.filter(
            same_room_filter
            & (
                entry_between_date_filter
                | exit_between_date_filter
            )
        )
    
        exposed_attendees.extend(exposed_people)

    return exposed_attendees

@shared_task
def get_rooms_and_dates(suspect_email, exposure_date):
    """"Get all the attendee records of the suspect
    and arrange them in an object"""
    records = AttendanceRecord.objects.filter(
        attendee_email=suspect_email,
        entry_datetime__gte=exposure_date
    )

    attendance_info = list(
        map(
            (lambda registry: {
                'room': registry.room,
                'entry_datetime': registry.entry_datetime,
                'exit_datetime': registry.exit_datetime
            }),
            records
        )
    )

    return attendance_info