# events/serializers.py

import datetime
from rest_framework import serializers
from .models import Event, Ticket, User

class EventSerializer(serializers.ModelSerializer):
    # booking_posted=serializers.DateField(initial=datetime.date.now())
    class Meta:
        model = Event
        exclude = ('booking_posted', )
class TicketSerializer(serializers.ModelSerializer):
    # booked_at=serializers.DateField(initial=datetime.date.now())
    class Meta:
        model = Ticket
        exclude = ('booked_at', )
        
