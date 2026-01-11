from typing import Protocol
from domain.order import Order
from domain.money import Money

class OrderRepository(Protocol):
    def get_by_id(self, order_id: str) -> Order: ...
    def save(self, order: Order) -> None: ...

class PaymentGateway(Protocol):
    def charge(self, order_id: str, money: Money) -> bool: ...
