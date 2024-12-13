from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class OrderWasNotCreatedException(LogicException):

    @property
    def message(self):
        return f'Order was not created exception'