from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet

from perfil.api.serializers import PerfilSerializer

Usuario = get_user_model()


class Perfil2ViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get_object(self):
        return self.queryset.get(email=self.request.user)


class PerfilViewSet(ReadOnlyModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
