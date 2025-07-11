from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

from api.views import graphql_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', graphql_view),
    path('', RedirectView.as_view(url='/graphql', permanent=False)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
