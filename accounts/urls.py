from django.urls import path

from accounts.views import RegistrationView

app_name: str = 'accounts'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration_page')
]
