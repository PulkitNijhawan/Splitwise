from uuid import uuid4

from marshmallow import Schema, fields
from pymongo.collection import Collection

from app import db
from app.models.base_model import BaseModel
from app.schemas import BaseUserSchema


class User(BaseModel):
    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        collection: Collection = db.users,
        schema: Schema = BaseUserSchema(),
    ) -> None:
        super().__init__(collection, schema)
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self) -> dict:
        """ """
        return {"name": self.name, "email": self.email, "phone": self.phone}
