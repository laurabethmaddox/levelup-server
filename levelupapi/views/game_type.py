"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type)
            return Response(serializer.data)
        except GameType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game_types = GameType.objects.all() # The game_types variable is now a list of GameType objects
        serializer = GameTypeSerializer(game_types, many=True) # Adding many=True lets the serializer know that a list vs. a single object is to be serialized
        return Response(serializer.data)


class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    # The Meta class holds the configuration for the serializer
    class Meta:
        # This tells the serializer to use the GameType model and to include the id and label fields.
        model = GameType
        fields = ('id', 'label')