from interfaces.user_interface import IUsersPersistence
from ... objects.user import User
from datetime import datetime


class UsersStubPersistence(IUsersPersistence):
    def __init__(self):
        self.users = []

    def add_user(
        self,
        username,
        profile_pic,
        preference_id  # Foreign key
    ):
        user_id = len(self.users)
        new_user = User(
            user_id,
            username,
            datetime.now(),
            profile_pic,
            preference_id
        )
        self.users.append(new_user)
        # Return User id
        return user_id

    def get_user(
        self,
        user_id
    ):
        if user_id >= 0 and user_id < len(self.users):
            return self.users[user_id]
        return None

    def remove_user(
        self,
        user_id
    ):
        if user_id >= 0 and user_id < len(self.users):
            self.users.pop(user_id)
