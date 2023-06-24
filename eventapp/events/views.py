# events/api.py

from datetime import date,timedelta
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Event, Ticket, User
from .serializers import EventSerializer, TicketSerializer
from django.core import serializers
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
         Get permissions for this user. This is used to determine whether or not the user is authenticated and can create / update / delete users.
        """
        if self.action == 'create' or self.action == 'update' or self.action == 'delete':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema( description='Output : Returns created Event with its ID, Role: [\"Admin\"]')
    def create(self, request):
        """
         @param request - The request that contains the resource to create.
         @return The response to the request with the newly created resource. " status " : " 201 Created "
        """
        data=request.data
        data['booking_posted']=date.today()
        serializer=self.get_serializer(data=data)
        serializer.is_valid()
        serializer.save()

        return Response({"message":"event created sucessfull","data":serializer.data},status=status.HTTP_201_CREATED)

    @extend_schema( description='Param: Event ID, Output : Returns updated Event, Role: [\"Admin\"]')
    def update(self, request, *args,**kwargs):
        """
         Update an existing record. This is a method to be overridden by subclasses that need to handle an update of an existing record.
         @param request - The request for this update.
         @param pk - The primary key of the record to update.
         @return The response to the update request.
        """
        return super().update(request,*args,**kwargs)

    @extend_schema( description='Output : Return all available events, Role: [\"Authenticated User\"]')
    def list(self, request):
        """
         List resources. This is a paginated view of resource information. 
         @param request - The request to use when making the list call.
         @return The response to the list call as a list of Events containing the list of resources
        """
        return super().list(request)
    @extend_schema( description='Param: Event ID, Output : Returns Event Details, Role: [\"Authenticated User\"]')
    def retrieve(self, request, pk):
        """
         Retrieve a record by primary key. This is a low - level method to be used by client code that wishes to retrieve an existing record without needing to re - create it.
         @param request - The request for this request. It contains the user who made the request and the session which initiated this request.
         @param pk - The primary key of the record to retrieve.
        """
        return super().retrieve(request,pk)
    @extend_schema( description='Param: Event ID, Output : Returns updated Event, Role: [\"Admin\"]')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema( description='Param: Event ID, Output : No content, Role: [\"Admin\"]')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        """
         Get permissions for this user. This is used to determine whether or not the user is authenticated and can create / update / delete Tickets.
        """
        if self.action == 'update':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @extend_schema( description='Output : Return all booked tickets, Role: [\"Authenticated User\"]')
    def list(self, request, *args, **kwargs):
        # tickets=Ticket.objects.all()
        # data = serializers.serialize('json', tickets)
        # return Response({"data":data},status=status.HTTP_200_OK)
        return super().list(request)
    @extend_schema( description='Output : delete booked tickets, Role: [\"Adim\"]')
    def destroy(self, request, *args, **kwargs):
        sku_id = self.kwargs['pk']
        ticket=Ticket.objects.get(id=sku_id)
        
        event=Event.objects.get(id=ticket.event_id)
        last_day_to_delete=event.booking_posted+timedelta(days=10)
        if(date.today()>last_day_to_delete):
            return Response({"message":"user cannot delete ticket"},status=status.HTTP_403_FORBIDDEN)
        event.max_seats+=1
        event.save()
        self.perform_destroy(ticket)
        return Response({"message":"ticket deleted succesfully"},status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        ticket=self.get_object()
        data=request.data
        data['booked_at']=date.today()
        serializer=self.get_serializer(ticket,data=data)
        serializer.is_valid()
        serializer.save()
        return Response({"message":"ticekt updated"},status=status.HTTP_202_ACCEPTED)
    @extend_schema(description="")                    
    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event')
        user_id = request.data.get('user')
        event = Event.objects.get(id=event_id)
        if event.max_seats <= 0:
            response = HttpResponse('No available seats for this event.')
            response.status_code = 400
            return response
        data=request.data
        data['booked_at']=date.today()
        serializer=self.get_serializer(data=data)
        serializer.is_valid()
        last_day_to_book=event.booking_posted+timedelta(days=5)
        if(date.today()<=last_day_to_book):
            serializer.save()
            event.max_seats-=1
            event.save()
            return Response({"message":"ticket created for the event"},status=status.HTTP_201_CREATED)
        return Response({"message":"ticket bookings closed"},status=status.HTTP_400_BAD_REQUEST)
