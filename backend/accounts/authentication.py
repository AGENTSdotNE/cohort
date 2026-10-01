from rest_framework.authentication import SessionAuthentication as BaseSessionAuthentication


class SessionAuthentication(BaseSessionAuthentication):
    """Returns 401 rather than DRF's default 403, so the frontend can tell 'signed out' from 'forbidden'."""

    def authenticate_header(self, request):
        return 'Session'
