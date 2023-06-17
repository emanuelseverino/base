from django.urls import include, path
from rest_framework import routers
from perfil.api.viewsets import PerfilViewSet, Perfil2ViewSet

router = routers.DefaultRouter()
router.register(r'', PerfilViewSet)
router.register(r'meu', Perfil2ViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
