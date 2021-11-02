from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Account


class Game(models.Model):
    class BetChoices(models.TextChoices):
        NONE = None
        HOME: str = 'HOME', _('Home')
        AWAY: str = 'AWAY', _('Away')
        DRAW: str = 'DRAW', _('Draw')

    player = models.ForeignKey(Account, related_name='game', on_delete=models.CASCADE)
    bet_choice = models.CharField(max_length=4, choices=BetChoices.choices, default=BetChoices.NONE)
    bet_amount = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0))
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.player} - {self.bet_choice} - {self.bet_amount}$'
