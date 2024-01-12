from marshmallow import (EXCLUDE, Schema, ValidationError, fields, validate,
                         validates, validates_schema)

from app.constants import TOTAL_PERCENTAGE_EXPENSE
from app.enums import ExpensesEnum


class BaseSchema(Schema):
    """
    Base Schema
    """

    class Meta:
        """
        Meta class for BaseSchema. Provides various options for serializing attributes.
        """

        unknown = EXCLUDE


class BaseUserSchema(BaseSchema):
    name = fields.String(required=True)
    email = fields.Email(requred=True)
    phone = fields.String(required=True)

    @validates("phone")
    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) < 10 or len(value) > 15:
            raise ValidationError(
                "Invalid phone number. Please enter a valid phone number."
            )


class BaseExpenseSchema(BaseSchema):
    paid_by = fields.String(required=True)
    expense_type = fields.String(
        required=True,
        validate=validate.OneOf([expense_type.value for expense_type in ExpensesEnum]),
    )
    owed_by = fields.List(fields.String, required=True)
    amount = fields.Float(required=True)
    simplify = fields.Boolean(load_default=False)


class ExactExpenseSchema(BaseExpenseSchema):
    expenses = fields.List(fields.Float, required=True)

    @validates_schema
    def validate_exact_expense(self, data, **_):
        expenses = data.get("expenses", [])
        owed_by = data.get("owed_by", [])
        if len(expenses) != len(owed_by):
            raise ValidationError("In exact expense share of each person is required.")

        if sum(expenses) != data.get("amount"):
            raise ValidationError(
                "Total amount and total expenses by each person are not equal."
            )


class PercentExpenseSchema(BaseExpenseSchema):
    percentages = fields.List(fields.Float, required=True)

    @validates_schema
    def validate_percentage_expense(self, data, **_):
        percentages = data.get("percentages", [])
        owed_by = data.get("owed_by", [])
        if len(percentages) != len(owed_by):
            raise ValidationError(
                "In percentage expense share of each person is required."
            )

        if sum(percentages) != TOTAL_PERCENTAGE_EXPENSE:
            raise ValidationError("Total percentage out of bound.")


class TransactionSchema(BaseSchema):
    source = fields.String(required=True)
    destination = fields.String(required=True)
    amount = fields.List(fields.Float, required=True)


class GetAllTransactionRequestSchema(BaseSchema):
    simplify = fields.Boolean(load_default=False)


class GetTransactionRequestSchema(GetAllTransactionRequestSchema):
    source = fields.String(required=True)
