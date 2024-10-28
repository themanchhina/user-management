from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .errors import UserNotFoundError, InvalidUserDataError
from .serializers import UserSerializer
from .repository import UserRepository


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer

    def list(self, request):
        users = UserRepository.get_all_users()
        return Response(UserSerializer(users, many=True).data)

    def retrieve(self, request, pk=None):
        user = UserRepository.get_user_by_id(pk)
        if user is None:
            raise UserNotFoundError(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = UserRepository.create_user(
                name=serializer.validated_data['name'],
                date_of_birth=serializer.validated_data['date_of_birth']
            )
            response_serializer = UserSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise InvalidUserDataError(serializer.errors)

    def update(self, request, pk=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = UserRepository.update_user(
                user_id=pk,
                name=serializer.validated_data.get('name'),
                date_of_birth=serializer.validated_data.get('date_of_birth')
            )
            if user is None:
                raise UserNotFoundError(pk)
            response_serializer = UserSerializer(user)
            return Response(response_serializer.data)
        else:
            raise InvalidUserDataError(serializer.errors)

    def destroy(self, request, pk=None):
        success = UserRepository.delete_user(pk)
        if not success:
            raise UserNotFoundError(pk)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
