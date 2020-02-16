from interfaces.user_interface import IUsersPersistence


class UsersPersistence(IUsersPersistence):

    def add_user(
        self,
        username,
        profile_pic,
        preference_id  # Foreign key
    ):
        # Return User id
        pass

    def get_user(
        self,
        user_id
    ):
        pass

    def remove_user(
        self,
        user_id
    ):
        pass
