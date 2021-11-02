from rest_framework import serializers

from footballStudio.models import Game


class GameSerializer(serializers.ModelSerializer):
    player = serializers.ReadOnlyField(source='account.email')

    class Meta:
        model = Game
        fields = ['player', 'bet_choice', 'bet_amount']
