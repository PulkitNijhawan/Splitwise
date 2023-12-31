from app.api.users.base import UserService
from app.models.users import User
from app.utils.helpers import make_response


class CreateUser(UserService):
    def set_user(self):
        self.user = User(**self.validated_data)

    def process(self):
        super().process()
        self.create_user()
        return {"id": self.user.id, **self.user.to_dict()}
