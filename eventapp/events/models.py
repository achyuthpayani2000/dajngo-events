from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

class User(AbstractUser):
    pass

### Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)
    max_seats = models.PositiveIntegerField(default=0)
    booking_posted=models.DateField(default=date.today())
#Ticket Model
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booked_at = models.DateField(default=date.today()) 