from app import db
from app.api.split.base import TransactionService
from app.models.split import Transaction
from app.utils.helpers import make_response


class GetTransaction(TransactionService):
    """ """

    def __init__(self, validated_data: dict, destination: str = None) -> None:
        super().__init__(validated_data)
        self.source = validated_data["source"]
        self.destination = destination

    def set_transactions(self):
        """ """
        query = db.transaction
        if self.source and self.destination:
            query = query.find_one(
                {
                    "$or": [
                        {"source": self.source, "destination": self.destination},
                        {"source": self.destination, "destination": self.source},
                    ]
                },
                {"_id": 1},
            )
        elif self.source or self.destination:
            query = query.find(
                {
                    "$or": [
                        {"source": self.source or self.destination},
                        {"destination": self.source or self.destination},
                    ]
                },
                {"_id": 1},
            )
        else:
            query = query.find({}, {"_id": 1})

        self.transactions = [Transaction.get(query_doc["_id"]) for query_doc in query]

    def process(self) -> list:
        super().process()
        return self.transactions if self.destination else self.generate_statement()
