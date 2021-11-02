from enum import Enum
import random
from typing import Union


class Suites(Enum):
    Club = '♣'
    Spade = '♠'
    Diamond = '♦'
    Heart = '♥'


class Card:
    """ Card class that initialize suit and rank and than represents them in appropriate visuals """

    def __init__(self, rank: int, suit: str) -> None:
        """
        :param rank: card rank :type int
        :param suit: card suit :type str
        """
        self.suit = suit
        self.rank = rank

    def __repr__(self) -> str:
        """ :returns cards in appropriate visual (...A♣, A♠, A♦, A♥) """
        return f'{self.rank}{self.suit}'


class CardSerializer:

    def __init__(self, rank: int) -> None:
        self.rank = rank

    def serialize(self) -> Union[int, str]:
        """
        Method that serializes cards in appropriate format (int to str)
        :returns - self.rank to str if rank in dict.keys (J, Q, K, A); Otherwise: self.rank
        """
        to_string = {
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A',
        }.get(self.rank, self.rank)  # If rank not in dict it takes itself (11 - J; 9 - 9...)

        return to_string


class Deck:
    """ Class Deck that initializes and then shuffles deck of cards """

    def __init__(self) -> None:
        self.deck = [str(Card((CardSerializer(rank).serialize()), suit.value)) for rank in range(2, 15)
                     for suit in Suites]
        random.shuffle(self.deck)


class FootballStudioGame(Deck):
    """ Main class for gambling game football studio game """

    home_card = None
    away_card = None
    away_win_count = 0
    home_win_count = 0
    draw_win_count = 0

    @staticmethod
    def to_int(card_rank: str) -> int:
        """
        :param card_rank string (J, Q, K, A)
        :returns - Converted card rank to int (Input: str(A) -> Output: int(14)...)
        """
        r = {
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14,
        }.get(card_rank, card_rank)  # If rank not in dict it takes itself (11 - J; 9 - 9...)
        return int(r)

    def winner(self) -> str:
        """
        :returns type:str winner table combination (HOME, AWAY, DRAW)
        """
        home_card_rank: str = self.home_card[:-1]
        away_card_rank: str = self.away_card[:-1]

        if self.to_int(home_card_rank) > self.to_int(away_card_rank):
            self.home_win_count += 1
            return 'HOME'
        elif self.to_int(home_card_rank) < self.to_int(away_card_rank):
            self.away_win_count += 1
            return 'AWAY'
        elif self.to_int(home_card_rank) == self.to_int(away_card_rank):
            self.draw_win_count += 1
            return 'DRAW'


def main():
    """ TESTING """
    c = FootballStudioGame()
    assert c.to_int('J') == 11
    assert c.to_int('Q') == 12
    assert c.to_int('K') == 13
    assert c.to_int('A') == 14
    assert c.to_int('11') == 11
    assert c.to_int('8') == 8
    c.home_card = c.deck.pop()
    c.away_card = c.deck.pop()

    print(c.winner())


game = FootballStudioGame()

if __name__ == '__main__':
    main()
