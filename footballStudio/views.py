from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from footballStudio.cards import FootballStudioGame
from footballStudio.models import Game
from footballStudio.serializers import GameSerializer

cards = FootballStudioGame()


class FootballStudioTableView(APIView):
    """ @TODO: doc """

    def get(self, request, **kwargs):
        cards.home_card = cards.deck.pop()
        cards.away_card = cards.deck.pop()

        data = {
            'deck_length': len(cards.deck),
            'winner': cards.winner(),
            'home_card': cards.home_card,
            'away_card': cards.away_card,
            'away_count': cards.away_win_count,
            'home_count': cards.home_win_count,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class FootballStudioBetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                'bet_choice': str(Game.BetChoices.choices),
                'balance': request.user.balance
            }
        )

    def post(self, request, **kwargs):
        serializer = GameSerializer(data=request.data)

        if serializer.is_valid():
            player = serializer.save(player=request.user)

            if request.user.balance == 0:
                raise ValidationError({'balance': 'Balance is empty'})
            elif player.bet_amount < 5:
                raise ValidationError({'bet_amount': 'Bet amount must be more than 5$'})
            elif request.user.balance < player.bet_amount:
                raise ValidationError({'balance': 'Balance is less than amount'})

            self.request.user.balance = self.request.user.balance - player.bet_amount
            self.request.user.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
{
    "player": "admin@example.com",
    "bet_choice": "HOME",
    "bet_amount": 10
}
'''
