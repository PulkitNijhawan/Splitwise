from abc import ABC, abstractmethod

from app.models.split import Transaction
from app.utils.helpers import MaxHeap, generate_balance, make_response
from app.utils.transactions_simplifier import TransactionSimplifier


class TransactionService(ABC):
    def __init__(self, validated_data: dict) -> None:
        self.transactions: list[Transaction] = None
        self.simplify: bool = validated_data["simplify"]

    @abstractmethod
    def set_transactions(self):
        """ """

    def save_transactions(self):
        for transaction in self.transactions:
            transaction.save()

    def generate_statement(self) -> list[str]:
        statement = []
        for transaction in self.transactions:
            total_amount = sum(transaction.amount)
            statement.append(
                f"{transaction.source.name} owes {transaction.destination.name} Rs.{total_amount}"
                if total_amount > 0
                else f"{transaction.destination.name} owes {transaction.source.name} Rs.{total_amount}"
            )
        return statement

    def generate_balance(self) -> dict[str, float]:
        """ """
        balance_sheet = {}

        for transaction in self.transactions:
            transfer_amount: float = sum(transaction.amount)
            balance_sheet[transaction.source.id] = balance_sheet.get(
                transaction.source.id, 0
            ) + (-transfer_amount)
            balance_sheet[transaction.destination.id] = (
                balance_sheet.get(transaction.destination.id, 0) + transfer_amount
            )

        return balance_sheet

    def simplify_transactions(self):
        """ """
        balance_sheet = generate_balance(self.transactions)
        self.transactions = TransactionSimplifier(balance_sheet).simplify()

    def process(self):
        """ """
        self.set_transactions()
