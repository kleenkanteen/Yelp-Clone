from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.core.exceptions import ValidationError


from accounts.models import CustomUser


# serializers for the accounts - custom user
class AccountSerializer(ModelSerializer):
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        min_length=8,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
        )

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'first_name', 'last_name', 'avatar', 'email']

    def create(self, validated_data):

        if validated_data['password'] != validated_data['password2']:
            raise ValidationError({
                'password': "The two password fields didn't match"
            })
        validated_data.pop('password2')
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user