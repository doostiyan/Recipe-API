from rest_framework.generics import CreateAPIView

from users.serializers.user import UserSerializer


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer