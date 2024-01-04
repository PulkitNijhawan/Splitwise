import heapq
from dataclasses import dataclass

from app.models.split import Transaction


class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, value):
        heapq.heappush(self.heap, (-value[1], value))

    def extract_max(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        return None

    def is_empty(self):
        return not bool(self.heap)


@dataclass
class UserBalance:
    id: str
    balance: float


class TransactionSimplifier:
    def __init__(self, balance_sheet: dict) -> None:
        """ """
        self.positive_category = MaxHeap()
        self.negative_category = MaxHeap()
        for id, balance in balance_sheet.items():
            if balance < 0:
                self.negative_category.insert([id, -balance])
            elif balance > 0:
                self.positive_category.insert([id, balance])

    def simplify(self) -> list[Transaction]:
        new_transactions: list[Transaction] = []
        while not self.positive_category.is_empty():
            receiver = self.positive_category.extract_max()
            sender = self.negative_category.extract_max()

            amount_transferred = min(receiver[1], sender[1])

            new_transactions.append(
                Transaction(
                    source=sender[0],
                    destination=receiver[0],
                    amount=[amount_transferred],
                )
            )

            sender[1] -= amount_transferred
            receiver[1] -= amount_transferred

            if sender[1]:
                self.negative_category.insert(sender)
            if receiver[1]:
                self.positive_category.insert(receiver)

        return new_transactions
