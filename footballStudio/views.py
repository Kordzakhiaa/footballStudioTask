from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from footballStudio.cards import FootballStudioGame
from footballStudio.models import Game
from footballStudio.serializers import GameSerializer

game = FootballStudioGame()


class FootballStudioTableView(APIView):
    """ @TODO: doc """

    def get(self, request, **kwargs):
        # cards.home_card = cards.deck.pop()
        # cards.away_card = cards.deck.pop()
        #
        # data = {
        #     'deck_length': len(cards.deck),
        #     'winner': cards.winner(),
        #     'home_card': cards.home_card,
        #     'away_card': cards.away_card,
        #     'away_count': cards.away_win_count,
        #     'home_count': cards.home_win_count,
        #     'draw_count': cards.draw_win_count,
        # }
        # return Response(data=data, status=status.HTTP_200_OK)
        return Response(data={'test': 'test'}, status=status.HTTP_200_OK)


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

            # @TODO create method that will provide this if/elif block
            if request.user.balance == 0:
                raise ValidationError({'balance': 'Balance is empty'})
            elif player.bet_amount < 5:
                raise ValidationError({'bet_amount': 'Bet amount must be more than 5$'})
            elif request.user.balance < player.bet_amount:
                raise ValidationError({'balance': 'Balance is less than amount'})

            game.home_card = game.deck.pop()
            game.away_card = game.deck.pop()

            if game.winner() == 'DRAW' and game.winner() == player.bet_choice:
                request.user.balance += player.bet_amount * 11
            elif game.winner() == 'DRAW' and game.winner() != player.bet_choice:
                request.user.balance += player.bet_amount / 2
            elif game.winner() != 'DRAW' and game.winner() == player.bet_choice:
                request.user.balance += player.bet_amount * 2
            elif game.winner() != player.bet_choice:
                request.user.balance -= player.bet_amount

            request.user.save()

            return Response(data={
                'serializer data': serializer.data,
                'winner': game.winner(),
                'my bet choice': player.bet_choice,
                'my bet amount': player.bet_amount,
                'home card': game.home_card,
                'away card': game.away_card,
                'my balance': request.user.balance
            }, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
{
    "bet_choice": "HOME",
    "bet_amount": 10
}
'''
