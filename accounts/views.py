from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.serializers import AccountSerializer

# view to create a new account
class CreateAccountView(CreateAPIView):
    serializer_class = AccountSerializer


# view to update an account
class UpdateAccountView(UpdateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


