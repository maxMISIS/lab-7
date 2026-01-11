from dataclasses import dataclass, field
from typing import List
from .order_line import OrderLine
from .money import Money
from .order_status import OrderStatus

class DomainError(Exception):
    pass

@dataclass
class Order:
    order_id: str
    lines: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.NEW

    def add_line(self, line: OrderLine) -> None:
        if self.status == OrderStatus.PAID:
            raise DomainError("Cannot modify order after payment")
        self.lines.append(line)

    def remove_line(self, index: int) -> None:
        if self.status == OrderStatus.PAID:
            raise DomainError("Cannot modify order after payment")
        self.lines.pop(index)

    @property
    def total(self) -> Money:
        if not self.lines:
            return Money(0, "EUR")
        currency = self.lines[0].unit_price.currency
        total_amount = 0
        for line in self.lines:
            if line.unit_price.currency != currency:
                raise DomainError("All order lines must have the same currency")
            total_amount += line.total.amount
        return Money(total_amount, currency)

    def pay(self) -> Money:
        if len(self.lines) == 0:
            raise DomainError("Cannot pay an empty order")
        if self.status == OrderStatus.PAID:
            raise DomainError("Order is already paid")
        self.status = OrderStatus.PAID
        return self.total
