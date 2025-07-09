from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from api.views import graphql_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', graphql_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
