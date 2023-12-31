from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from usuario.api.serializers import CustomAuthTokenSerializer, MudarSenhaSerializer, ChangePasswordSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


Usuario = get_user_model()


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = Usuario
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("senha_atual")):
                return Response({"senha_atual": "Digite a senha correta."}, status=HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("senha_nova"))
            self.object.save()
            response = {
                'messagem': 'Senha atualizada com sucesso.',
            }

            return Response(response)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
