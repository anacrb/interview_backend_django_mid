from typing import Optional

from interview.order.interface import OrderRepositoryInterface
from interview.order.models import Order


class DeactivateOrderUseCase:
    def __init__(self, order_repo: OrderRepositoryInterface):
        self.order_repo = order_repo

    def execute(self, order_id: int) -> Optional[Order]:
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValueError("Order ID must be a positive integer.")

        deactivated_order = self.order_repo.deactivate_order(order_id)
        return deactivated_order