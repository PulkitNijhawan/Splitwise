from http import HTTPStatus

from flask import Blueprint, Response, jsonify, request
from flask.views import MethodView
from marshmallow import Schema, ValidationError

from app.api.expenses.create_expense import (EqualExpense, ExactExpense,
                                             PercentExpense)
from app.api.split.read import GetTransaction
from app.api.users.create import CreateUser
from app.enums import ExpensesEnum
from app.schemas import (BaseExpenseSchema, BaseUserSchema, ExactExpenseSchema,
                         GetAllTransactionRequestSchema,
                         GetTransactionRequestSchema, PercentExpenseSchema)
from app.utils.helpers import make_response


class BaseView(MethodView):
    request_schema: Schema = None
    request_processor = None
    error_message: str = None
    success_message: str = None

    def handle_request(self, request_data: dict) -> tuple[Response, HTTPStatus]:
        import pdb

        pdb.set_trace()
        try:
            validated_data = self.request_schema.load(
                {**request_data, **request.view_args}
            )

        except ValidationError as err:
            return make_response(
                message=self.error_message,
                data=err.messages_dict,
                status_code=HTTPStatus.BAD_REQUEST,
            )

        return make_response(
            message=self.success_message,
            data=self.request_processor(validated_data).process(),
        )

    def post(self):
        request_data = {**request.get_json(), **request.view_args}
        return self.handle_request(request_data)

    def get(self):
        return self.handle_request(request.view_args)


class AddExpenseView(BaseView):
    error_message = "Failed to add expense!"
    success_message = "Expense added successfully!"

    def select_expense_type(self):
        expense_type: str = request.get_json().get("expense_type")
        match expense_type:
            case ExpensesEnum.PERCENTAGE:
                self.request_schema = PercentExpenseSchema()
                self.request_processor = PercentExpense

            case ExpensesEnum.EQUAL:
                self.request_schema = BaseExpenseSchema()
                self.request_processor = EqualExpense

            case ExpensesEnum.EXACT:
                self.request_schema = ExactExpenseSchema()
                self.request_processor = ExactExpense

    def post(self):
        self.select_expense_type()
        return super().post()


class CreateUserView(BaseView):
    request_schema = BaseUserSchema()
    request_processor = CreateUser
    error_message = "User registration failed!"
    success_message = "User registered successfully!"


class GetTransactionView(BaseView):
    request_schema = GetTransactionRequestSchema()
    request_processor = GetTransaction
    error_message = "Transaction fetch failed!"
    success_message = "Transaction fetch successful!"


class GetAllTransactionView(GetTransactionView):
    request_schema = GetAllTransactionRequestSchema()
