# Generated by Django 4.0.4 on 2022-05-10 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0007_alter_event_organizer'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(related_name='attendees', to='levelupapi.gamer'),
        ),
    ]
