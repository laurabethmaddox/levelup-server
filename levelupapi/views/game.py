"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all() # The game variable is now a list of Games objects
        
        # The request from the method parameters holds all the information fo the request from the client.
        # request.query_params - a dictionary of any query parameters that were in the url
        # .get - using on a dictionary is a way to find if a key is present on the dictionary.
        game_type = request.query_params.get('type', None)
        # If the 'type' key is not presented on the dictionary it will return None
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
            
        serializer = GameSerializer(games, many=True) # Adding many=True lets the serializer know that a list vs. a single object is to be serialized
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        # Is getting the game that is logged in. Then we use the request.auth.user to get the Gamer object based on the user.
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data) # request.data dictionary is passed to the new serializer instead of making a new instance of the Game model
        serializer.is_valid(raise_exception=True) # is_valid is to make sure the client sent valid data.
        serializer.save(gamer=gamer) # If code passes validation, the save method will add the game to the datbase and add an id to the serializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        serializer = CreateGameSerializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    # The Meta class holds the configuration for the serializer
    class Meta:
        # This tells the serializer to use the Game model and to include the id, game_type, title, maker, gamer, number_of_players, and skill_level fields.
        model = Game
        fields = ('id', 'game_type', 'title', 'maker', 'gamer', 'number_of_players', 'skill_level')
        depth = 1

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']