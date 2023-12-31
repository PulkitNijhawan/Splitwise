from abc import abstractmethod
from http import HTTPStatus

from flask import Response

from app.models.users import User


class UserService:
    def __init__(self, validated_data) -> None:
        self.validated_data = validated_data
        self.user: User = None

    def create_user(self) -> str:
        """ """
        return self.user.save()

    @abstractmethod
    def set_user(self):
        """ """

    def process(self) -> tuple[Response, HTTPStatus]:
        """ """
        self.set_user()
