# Generated by Django 3.2.5 on 2021-08-02 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddConstraint(
            model_name='building',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_building_name_constraint'),
        ),
        migrations.AddField(
            model_name='room',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.building'),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.UniqueConstraint(fields=('name', 'building'), name='unique_room_name_per_building_constraint'),
        ),
    ]
