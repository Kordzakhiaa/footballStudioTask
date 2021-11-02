from django.urls import path

from footballStudio.views import FootballStudioGameView

app_name: str = 'football_studio'

urlpatterns = [
    path('football_studio/', FootballStudioGameView.as_view(), name='football_studio_view')
]
