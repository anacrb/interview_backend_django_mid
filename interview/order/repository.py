from typing import List, Optional
from datetime import date

from interview.order.interface import OrderRepositoryInterface
from interview.order.models import Order, OrderTag


class DjangoOrderRepository(OrderRepositoryInterface):
    def get_orders_between_dates(self, query_start_date: date, query_embargo_date: date) -> List[Order]:
        if query_start_date > query_embargo_date:
            raise ValueError("Start date cannot be after end date.")

        return list(Order.objects.filter(
            start_date__lte=query_start_date,
            embargo_date__gte=query_embargo_date
        ).distinct())
