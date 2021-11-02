from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from footballStudio.cards import FootballStudioGame

cards = FootballStudioGame()


class FootballStudioGameView(APIView):
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
