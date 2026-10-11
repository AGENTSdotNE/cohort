from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from .views import frontend_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
]

# Django serves uploads itself so staging works too. A real production app keeps them in object storage.
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]

urlpatterns += [re_path(r'^(?!api/|admin/|media/|static/).*$', frontend_index)]
