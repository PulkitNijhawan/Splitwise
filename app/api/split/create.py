from app.api.split.base import TransactionService
from app.api.split.read import GetTransaction
from app.models.split import Transaction


class CreateTransaction(TransactionService):
    def __init__(self, validated_data: dict, new_transactions: list[dict]) -> None:
        super().__init__(validated_data)
        self.new_transactions = new_transactions

    def attach_new_transaction(
        self, saved_transaction: Transaction, new_transaction: dict
    ):
        """ """
        if (
            new_transaction["source"] == saved_transaction.source
            and new_transaction["destination"] == saved_transaction.destination
        ):
            saved_transaction.amount.append(new_transaction["amount"])
        else:
            saved_transaction.amount.append(-new_transaction["amount"])

    def set_each_transaction(self, new_transaction: str):
        if saved_transaction := GetTransaction(
            validated_data={
                "simplify": self.simplify,
                "source": new_transaction["source"],
            },
            destination=new_transaction["destination"],
        ).process():
            self.attach_new_transaction(saved_transaction, new_transaction["source"])
            return saved_transaction

        return Transaction(
            source=new_transaction["source"],
            destination=new_transaction["destination"],
            amount=new_transaction["amount"],
        )

    def set_transactions(self):
        """ """
        self.transactions = [
            self.set_each_transaction(new_transaction)
            for new_transaction in self.new_transactions
        ]

    def process(self):
        super().process()
        self.save_transactions()
        if self.simplify:
            self.save_transactions()
        return self.generate_statement()
