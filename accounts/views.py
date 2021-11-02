from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
