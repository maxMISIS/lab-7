import pytest

from domain.order import Order, DomainError
from domain.order_line import OrderLine
from domain.money import Money
from domain.order_status import OrderStatus

from application.pay_order_use_case import PayOrderUseCase
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


def test_successful_payment():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(True)
    uc = PayOrderUseCase(repo, gateway)

    order = Order("o1")
    order.add_line(OrderLine("p1", 2, Money(500, "EUR")))  # 10.00 EUR if cents
    order.add_line(OrderLine("p2", 1, Money(300, "EUR")))
    repo.add(order)

    result = uc.execute("o1")

    assert result.success is True
    assert repo.get_by_id("o1").status == OrderStatus.PAID
    assert len(gateway.charges) == 1
    assert gateway.charges[0][1].amount == 1300


def test_error_on_empty_order_payment():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(True)
    uc = PayOrderUseCase(repo, gateway)

    order = Order("o2")
    repo.add(order)

    result = uc.execute("o2")

    assert result.success is False
    assert "empty" in result.message.lower()
    assert len(gateway.charges) == 0


def test_error_on_double_payment():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(True)
    uc = PayOrderUseCase(repo, gateway)

    order = Order("o3")
    order.add_line(OrderLine("p1", 1, Money(100, "EUR")))
    repo.add(order)

    r1 = uc.execute("o3")
    r2 = uc.execute("o3")

    assert r1.success is True
    assert r2.success is False
    assert "already" in r2.message.lower()
    assert len(gateway.charges) == 1


def test_cannot_modify_after_payment():
    order = Order("o4")
    order.add_line(OrderLine("p1", 1, Money(100, "EUR")))
    order.pay()

    with pytest.raises(DomainError):
        order.add_line(OrderLine("p2", 1, Money(50, "EUR")))

    with pytest.raises(DomainError):
        order.remove_line(0)


def test_total_is_sum_of_lines():
    order = Order("o5")
    order.add_line(OrderLine("p1", 3, Money(200, "EUR")))  # 600
    order.add_line(OrderLine("p2", 2, Money(150, "EUR")))  # 300
    assert order.total.amount == 900
