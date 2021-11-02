from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from footballStudio.cards import FootballStudioGame, Deck
from footballStudio.models import Game
from footballStudio.serializers import GameSerializer

game = FootballStudioGame()


class FootballStudioBetView(APIView):
    """ Football Studio Game view that provides betting """

    permission_classes = [IsAuthenticated]

    @staticmethod
    def check_deck() -> bool:
        """ Static Method that checks if deck is less than 2. If it is it will charge """
        if len(game.deck) <= 2:
            return True
        return False

    def get(self, request):
        return Response(
            {
                'user': str(request.user),
                'bet_choice': str(Game.BetChoices.choices),
                'balance': request.user.balance
            }
        )

    def post(self, request, **kwargs):
        if self.check_deck():
            game.deck = Deck().deck()

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
            game.away_card = game.deck.pop()  # POP CARDS FROM DECK EVERY NEX BET
            game.calculate(game=game, request_user=request.user, player=player)

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
