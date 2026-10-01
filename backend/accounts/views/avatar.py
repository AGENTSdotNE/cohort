from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import AvatarSerializer, UserSerializer


class AvatarView(APIView):
    parser_classes = [MultiPartParser]

    def put(self, request):
        serializer = AvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_name = request.user.avatar.name
        request.user.avatar = serializer.validated_data['avatar']
        request.user.save(update_fields=['avatar'])

        # Only once the new picture is saved, so a failed upload never leaves the user pointing at a deleted file.
        if old_name:
            request.user.avatar.storage.delete(old_name)

        return Response(UserSerializer(request.user).data)

    def delete(self, request):
        request.user.avatar.delete(save=False)
        request.user.save(update_fields=['avatar'])

        return Response(UserSerializer(request.user).data)
