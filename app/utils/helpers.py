from flask import jsonify

from app.models.split import Transaction


def make_response(message, data=None, error=None, status_code=200):
    response = {"message": message, "data": data or {}}
    if error:
        response.update({"details": error})
    return jsonify(response), status_code


def generate_statement(transactions: list[Transaction]) -> list[str]:
    statement = []
    for transaction in transactions:
        total_amount = sum(transaction.amount)
        statement.append(
            f"{transaction.source.name} owes {transaction.destination.name} Rs.{total_amount}"
            if total_amount > 0
            else f"{transaction.destination.name} owes {transaction.source.name} Rs.{total_amount}"
        )
    return statement


def generate_balance(transactions: list[Transaction]) -> dict[str, float]:
    """ """
    balance_sheet = {}

    for transaction in transactions:
        transfer_amount: float = sum(transaction.amount)
        balance_sheet[transaction.source.id] = balance_sheet.get(
            transaction.source.id, 0
        ) + (-transfer_amount)
        balance_sheet[transaction.destination.id] = (
            balance_sheet.get(transaction.destination.id, 0) + transfer_amount
        )

    return balance_sheet


import heapq


class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, value):
        heapq.heappush(self.heap, (-value[0], value))

    def extract_max(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        return None

    def get_max(self):
        if self.heap:
            return self.heap[0][1]
        return None
