from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from .views import frontend_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
]

# Serves uploaded files while DEBUG is on. In production they belong in object storage, not on the web server.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^(?!api/|admin/|media/|static/).*$', frontend_index)]
