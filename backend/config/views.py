from django.conf import settings
from django.http import FileResponse, Http404


def frontend_index(request):
    index_file = settings.FRONTEND_BUILD_DIR / 'index.html'
    if not index_file.exists():
        raise Http404('The frontend has not been built.')
    return FileResponse(index_file.open('rb'), content_type='text/html')
