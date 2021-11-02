from django.urls import path

from footballStudio.views import FootballStudioTableView, FootballStudioBetView

app_name: str = 'football_studio'

urlpatterns = [
    path('table/', FootballStudioTableView.as_view(), name='game_table_page'),
    path('bet/', FootballStudioBetView.as_view(), name='game_bet_page')
]
