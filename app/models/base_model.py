from abc import abstractmethod

from bson import ObjectId
from marshmallow import Schema
from pymongo.collection import Collection


class BaseModel:
    def __init__(self, collection: Collection, schema: Schema) -> None:
        self.collection = collection
        self.schema = schema
        self.id = None

    def save(self) -> str:
        self.id = str(
            self.collection.insert_one(self.schema.load(self.to_dict())).inserted_id
        )
        return self.id

    @classmethod
    def get(cls, id: str):
        result = cls.collection.find_one({"_id": ObjectId(id)})

        if result:
            return cls(**result)
        else:
            return None

    @abstractmethod
    def to_dict(self) -> dict:
        """ """

    def to_json(self) -> dict:
        return self.schema.dump(self.to_dict())
