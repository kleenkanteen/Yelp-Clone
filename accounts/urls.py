from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.views import CreateAccountView, UpdateAccountView

app_name = 'accounts'

urlpatterns = [
    path('signup/', CreateAccountView.as_view(), name='signup'),
    path('update/', UpdateAccountView.as_view(), name='update'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]