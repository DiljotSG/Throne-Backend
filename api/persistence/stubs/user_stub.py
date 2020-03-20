from datetime import datetime
from typing import List, Optional

from ..interfaces.user_interface import IUsersPersistence
from ...objects.user import User


class UsersStubPersistence(IUsersPersistence):
    def __init__(self) -> None:
        self.users: List[User] = []

    def add_user(
        self,
        username: str,
        profile_pic: str,
        preference_id: int  # Foreign key
    ) -> int:
        user_id = len(self.users)
        new_user = User(
            user_id,
            username,
            datetime.now(),
            profile_pic,
            preference_id
        )
        self.users.append(new_user)
        return user_id

    def get_user(
        self,
        user_id: int
    ) -> Optional[User]:
        if user_id >= 0 and user_id < len(self.users) and \
           self.users is not None:
            return self.users[user_id]
        return None

    def get_id_by_username(
        self,
        username: str
    ) -> Optional[int]:
        for user in self.users:
            if user.username == username:
                return user.id
        return None

    def remove_user(
        self,
        user_id: int
    ) -> None:
        if user_id >= 0 and user_id < len(self.users):
            self.users.pop(user_id)
