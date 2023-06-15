from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from usuario.api.viewsets import CustomAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls'), ),
    # path('login/', obtain_auth_token),
    path('login/', CustomAuthToken.as_view(),),
    path('usuario/', include('usuario.urls'), ),
    path('contas/', include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
