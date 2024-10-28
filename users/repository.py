from django.core.exceptions import ObjectDoesNotExist

from users.errors import UserNotFoundError
from users.models import User


class UserRepository:
    @staticmethod
    def get_all_users(order_by='-created_at'):
        return User.objects.all().order_by(order_by)

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise UserNotFoundError(user_id)

    @staticmethod
    def create_user(name, date_of_birth):
        user = User(name=name, date_of_birth=date_of_birth)
        user.save()
        return user

    @staticmethod
    def update_user(user_id, name=None, date_of_birth=None):
        user = UserRepository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        if name is not None:
            user.name = name
        if date_of_birth is not None:
            user.date_of_birth = date_of_birth
        user.save()
        return user

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        user.delete()
        return True
