from django.urls import path

from accounts.views import RegistrationView, LoginView

app_name: str = 'accounts'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration_page'),
    path('login/', LoginView.as_view(), name='login_page'),
]
