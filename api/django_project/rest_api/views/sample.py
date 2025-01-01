from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from rest_api.serializers.sample import SampleSerializer

UserModel = get_user_model()


class SampleViewTest(RetrieveAPIView):
    permission_classes = [permissions.AllowAny]  # noqa: RUF012
    serializer_class = SampleSerializer

    def get(self) -> Response:
        return Response(
            data=SampleSerializer({"names": ["bill", "bob", "keanu", "logan"]}).data,
            status=status.HTTP_200_OK,
        )
