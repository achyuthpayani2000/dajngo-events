from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

#### Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    max_seats = models.PositiveIntegerField(default=0)

#Ticket Model
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)