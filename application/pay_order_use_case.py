from dataclasses import dataclass
from application.ports import OrderRepository, PaymentGateway
from domain.order import DomainError

@dataclass(frozen=True)
class PayOrderResult:
    success: bool
    message: str

class PayOrderUseCase:
    def __init__(self, repo: OrderRepository, gateway: PaymentGateway):
        self._repo = repo
        self._gateway = gateway

    def execute(self, order_id: str) -> PayOrderResult:
        order = self._repo.get_by_id(order_id)

        try:
            money_to_charge = order.pay()
        except DomainError as e:
            return PayOrderResult(False, str(e))

        charged = self._gateway.charge(order_id, money_to_charge)
        if not charged:
            return PayOrderResult(False, "Payment failed")

        self._repo.save(order)
        return PayOrderResult(True, "Payment successful")
