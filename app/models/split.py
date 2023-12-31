from marshmallow import Schema
from pymongo.collection import Collection

from app import db
from app.models.base_model import BaseModel
from app.models.users import User
from app.schemas import TransactionSchema


class Transaction(BaseModel):
    def __init__(
        self,
        source: str,
        destination: str,
        amount: list[float],
        collection: Collection = db.transactions,
        schema: Schema = TransactionSchema(),
    ) -> None:
        super().__init__(collection, schema)
        self.source = User.get(source)
        self.destination = User.get(destination)
        self.amount = amount

    def to_dict(self) -> dict:
        """ """
        return {
            "source": self.source.id,
            "destination": self.destination.id,
            "amount": self.amount,
        }
