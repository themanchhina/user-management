from django.apps import AppConfig
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from users.errors import UserNotFoundError, InvalidUserDataError


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


def get_response_message(status, message):
    return {
        'success': False,
        'error': {
            'code': status,
            'message': message,
        }
    }


def user_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = get_response_message(response.status_code, response.data.get('detail', 'An error occurred.'))
    else:
        if isinstance(exc, UserNotFoundError):
            code = status.HTTP_404_NOT_FOUND
            response = Response(get_response_message(code, exc.message), status=code)
        elif isinstance(exc, InvalidUserDataError):
            code = status.HTTP_404_NOT_FOUND
            response = Response(get_response_message(code, exc.message), status=code)
        else:
            code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = Response(get_response_message(code, 'Internal server error.'), status=code)
    return response
