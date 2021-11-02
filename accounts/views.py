from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Account
from accounts.serializers import RegistrationSerializer


class RegistrationView(APIView):
    """ Registration Page """

    def post(self, request, **kwargs):
        """
        :returns appropriate HTTP Response. If everything is valid status=200 otherwise status=400
        """
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """ Custom login """

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return refresh

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Please fill all fields'}, status=status.HTTP_400_BAD_REQUEST)

        check_user = Account.objects.filter(email=email).exists()
        if not check_user:
            return Response({'error': 'Email does not exists'}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)

            refresh_token = self.get_tokens_for_user(request.user)

            data = {
                'refresh_token': str(refresh_token),
                'access_token': str(refresh_token.access_token),
                'user_email': request.user.email,
                'id': request.user.pk
            }
            return Response({'success': 'Successfully logged in', 'data': data}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid login details'}, status=status.HTTP_400_BAD_REQUEST)
