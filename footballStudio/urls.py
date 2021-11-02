from django.urls import path

from footballStudio.views import FootballStudioBetView

app_name: str = 'football_studio'

urlpatterns = [
    path('bet/', FootballStudioBetView.as_view(), name='game_bet_page')
]
