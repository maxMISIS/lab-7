from typing import Dict
from domain.order import Order

class InMemoryOrderRepository:
    def __init__(self):
        self._storage: Dict[str, Order] = {}

    def add(self, order: Order) -> None:
        self._storage[order.order_id] = order

    def get_by_id(self, order_id: str) -> Order:
        return self._storage[order_id]

    def save(self, order: Order) -> None:
        self._storage[order.order_id] = order
