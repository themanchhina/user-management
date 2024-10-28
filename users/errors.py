class UserNotFoundError(Exception):
    def __init__(self, id):
        self.message = f'User with id {id} not found'
