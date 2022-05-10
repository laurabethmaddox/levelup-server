"""View module for handling requests about events"""
from tkinter import E
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from levelupapi.models import Event, event
from levelupapi.models import Gamer


class EventView(ViewSet):
    """Level up events view"""
    # A view's job is to handle requests appropriate to the HTTP verb and the resource

    # method overriding
    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        # Get data from the DB (using the ORM (via the model) and convert it to JSON  (using the serializer) and then send that JSON back to the client ( using HTTP )
        try:
            event = Event.objects.get(pk=pk) # Data from the DB using ORM
            serializer = EventSerializer(event) # Converts event to JSON using the serializer
            return Response(serializer.data) # JSON to be sent back to the client using HTTP
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all() # The events variable is now a list of Event objects
        
        game = request.query_params.get('game', None)
        if game is not None:
            events = events.filter(game_id=game)
            
        serializer = EventSerializer(events, many=True) # Adding many=True lets the serializer know that a list vs. a single object is to be serialized
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized event instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # With Django REST you can create a custom action that your API will support by using @action above a method within a ViewSet
    # Using the action decorator turns a method into a new route
    # The route is named after the function. To call this method the url would be "http://localhost:8000/events/2/signup"
    @action(methods=['post'], detail=True) # In this case, the action will accept POST methods and because deatil=True the url will include the pk
    def signup(self, request, pk): # We need to know which event the user wants to sign up for we'll need to have th pk
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user) # We get the gamer that's logged in
        event = Event.objects.get(pk=pk) # We get the event by it's pk
        event.attendees.add(gamer) # The add method creates the relationship between this event and gamer by adding the event_id and gamer_id to the join table
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED) # The response sends back a 201 status code

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    # The Meta class holds the configuration for the serializer
    class Meta:
        # This tells the serializer to use the Event model and to include the id, game, description, date, time, and organizer fields.
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
        depth = 2

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'game', 'description', 'date', 'time', 'organizer']