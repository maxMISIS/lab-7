from domain.money import Money

class FakePaymentGateway:
    def __init__(self, should_succeed: bool = True):
        self.should_succeed = should_succeed
        self.charges = []

    def charge(self, order_id: str, money: Money) -> bool:
        self.charges.append((order_id, money))
        return self.should_succeed
