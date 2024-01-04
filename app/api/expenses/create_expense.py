from abc import abstractmethod

from app import db
from app.api.split.create import CreateTransaction
from app.enums import ExpensesEnum
from app.models.expenses import (EqualExpense, ExactExpense, Expense,
                                 PercentExpense)
from app.models.split import Transaction
from app.utils.helpers import (generate_balance, generate_statement,
                               make_response)


class BaseExpense:
    """ """

    expense_type = None

    def __init__(self, validated_data: dict) -> None:
        self.validated_data = validated_data
        self.simplify = validated_data.pop("simplify")
        self.expense: Expense = self.expense_type(**self.validated_data)

    def create_response(self):
        """ """
        return make_response(
            message="Expense added successfully!",
            data=generate_statement(self.transactions),
        )

    def create_expense(self):
        self.expense.save()

    @abstractmethod
    def calculate_transactions(self) -> list[dict]:
        """ """

    def process(self):
        """ """
        new_transactions: list[dict] = self.calculate_transactions()
        return CreateTransaction(
            validated_data={"simplify": self.simplify},
            new_transactions=new_transactions,
        ).process()


class EqualExpense(BaseExpense):
    expense_type = EqualExpense

    def calculate_transactions(self):
        new_transactions = []
        amount_owed: float = round(
            self.expense.amount / (len(self.expense.owed_by) + 1), 2
        )
        for owed_by in self.expense.owed_by:
            new_transactions.append(
                {
                    "source": owed_by,
                    "destination": self.expense.paid_by,
                    "amount": amount_owed,
                }
            )

        return new_transactions


class ExactExpense(BaseExpense):
    expense_type = ExactExpense

    def calculate_transactions(self):
        new_transactions = []
        for owed_by, amount_owed in list(
            zip(self.expense.owed_by, self.expense.expenses)
        ):
            new_transactions.append(
                {
                    "source": owed_by,
                    "destination": self.expense.paid_by,
                    "amount": amount_owed,
                }
            )

        return new_transactions


class PercentExpense(BaseExpense):
    expense_type = PercentExpense

    def calculate_transactions(self):
        amounts_owed: list[float] = [
            round((self.expense.amount * percentage) / 100, 2)
            for percentage in self.expense.percentages
        ]
        new_transactions = []
        for owed_by, amount_owed in list(zip(self.expense.owed_by, amounts_owed)):
            new_transactions.append(
                {
                    "source": owed_by,
                    "destination": self.expense.paid_by,
                    "amount": amount_owed,
                }
            )

        return new_transactions
