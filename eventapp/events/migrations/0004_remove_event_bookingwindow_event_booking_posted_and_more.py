# Generated by Django 4.2.2 on 2023-06-24 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_ticket_booked_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='bookingwindow',
        ),
        migrations.AddField(
            model_name='event',
            name='booking_posted',
            field=models.DateField(default=datetime.date(2023, 6, 24)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='booked_at',
            field=models.DateField(default=datetime.date(2023, 6, 24)),
        ),
    ]