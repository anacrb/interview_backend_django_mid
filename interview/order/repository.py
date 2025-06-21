from typing import Optional

from interview.order.interface import OrderRepositoryInterface
from interview.order.models import Order


class DjangoOrderRepository(OrderRepositoryInterface):

    def deactivate_order(self, order_id: int) -> Optional[Order]:
        try:
            order = Order.objects.get(id=order_id)
            if order.is_active:
                order.is_active = False
                order.save()
            return order
        except Order.DoesNotExist:
            return None