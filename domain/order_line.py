from dataclasses import dataclass
from .money import Money

@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: int
    unit_price: Money

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be > 0")

    @property
    def total(self) -> Money:
        return Money(self.unit_price.amount * self.quantity, self.unit_price.currency)
