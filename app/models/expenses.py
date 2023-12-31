from marshmallow import Schema
from pymongo.collection import Collection

from app import db
from app.models.base_model import BaseModel
from app.models.users import User
from app.schemas import (BaseExpenseSchema, ExactExpenseSchema,
                         PercentExpenseSchema)


class Expense(BaseModel):
    def __init__(
        self,
        paid_by: str,
        expense_type: str,
        owed_by: list[str],
        amount: float,
        collection: Collection = db.expenses,
        schema: Schema = BaseExpenseSchema(),
    ) -> None:
        super().__init__(collection, schema)
        self.paid_by = User.get(paid_by)
        self.expense_type = expense_type
        self.owed_by = [User.get(owed) for owed in owed_by]
        self.amount = amount

    def to_dict(self) -> dict:
        return {
            "paid_by": self.paid_by.id,
            "expense_type": self.expense_type,
            "owed_by": [owed_by.id for owed_by in self.owed_by],
            "amount": self.amount,
        }


class EqualExpense(Expense):
    """ """


class ExactExpense(Expense):
    """ """

    def __init__(
        self,
        paid_by: str,
        expense_type: str,
        owed_by: list[str],
        amount: float,
        expenses: list[float],
        collection: Collection = db.expenses,
        schema: Schema = ExactExpenseSchema,
    ) -> None:
        super().__init__(paid_by, expense_type, owed_by, amount, collection, schema)
        self.expenses = expenses

    def to_dict(self) -> dict:
        expense_dict = super().to_dict()
        return {**expense_dict, "expenses": self.expenses}


class PercentExpense(Expense):
    """ """

    def __init__(
        self,
        paid_by: str,
        expense_type: str,
        owed_by: list[str],
        amount: float,
        percentages: list[float],
        collection: Collection = db.expenses,
        schema: Schema = PercentExpenseSchema,
    ) -> None:
        super().__init__(paid_by, expense_type, owed_by, amount, collection, schema)
        self.percentages = percentages

    def to_dict(self) -> dict:
        expense_dict = super().to_dict()
        return {**expense_dict, "expenses": self.percentages}
