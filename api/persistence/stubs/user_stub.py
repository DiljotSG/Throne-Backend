from interfaces.user_interface import IUsersPersistence
from ... objects.user import User


class UsersPersistence(IUsersPersistence):
    def __init__(self):
        self.users = []

    def add_user(
        self,
        username,
        profile_pic,
        preference_id  # Foreign key
    ):
        user_id = len(self.users)
        new_user = User(user_id, username, profile_pic, preference_id)
        self.users.append(new_user)
        # Return User id
        return user_id

    def get_user(
        self,
        user_id
    ):
        return self.users[user_id]

    def remove_user(
        self,
        user_id
    ):
        self.users.pop(user_id)
