class UserNotFoundError(Exception):
    def __init__(self, id):
        self.message = f'User with id {id} not found'


class InvalidUserDataError(Exception):
    def __init__(self, message):
        self.message = message
