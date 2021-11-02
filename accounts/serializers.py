from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            "email": {
                "validators": [
                    EmailValidator,
                    UniqueValidator(
                        queryset=Account.objects.all(),
                        message="This email already exist!"
                    )
                ]
            }
        }

    def save(self, **kwargs):
        account = Account(
            email=self.validated_data['email'],
        )
        password = self.validated_data['password'],
        password2 = self.validated_data['password2'],

        if password[0] != password2[0]:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        account.set_password(password[0])
        account.save()

        return account
