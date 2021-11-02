from rest_framework import serializers

from footballStudio.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['player', 'bet']
