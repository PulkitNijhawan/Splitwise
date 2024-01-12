"""
Module to register routes
"""

from flask import Blueprint
from flask.app import Flask

from app.main import AddExpenseView, CreateUserView, GetTransactionView


def register_routes(app: Flask) -> None:
    """
    Function to register routes

    Args:
        app (Flask): Flask app
    """

    service_bp = Blueprint("service-blueprint", __name__, url_prefix=f"/{app.config["SITE_NAME"].lower()}")
    service_bp.add_url_rule(rule="/user", view_func=CreateUserView.as_view("create_user_view"), methods=["POST"])
    service_bp.add_url_rule(rule="/expense", view_func=AddExpenseView.as_view("add_expense_view"), methods=["POST"])
    service_bp.add_url_rule(rule="/transaction/<transaction_id>", view_func=GetTransactionView.as_view("get_transaction_view"), methods=["GET"])
    service_bp.add_url_rule(rule="/transactions", view_func=GetTransactionView.as_view("get_transactions_view"), methods=["GET"])

    app.register_blueprint(service_bp)
