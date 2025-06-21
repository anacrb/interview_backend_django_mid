from typing import List
from datetime import date

from interview.order.interface import OrderRepositoryInterface
from interview.order.models import Order

class GetOrdersByDateRangeUseCase:
    def __init__(self, order_repo: OrderRepositoryInterface):
        self.order_repo = order_repo

    def execute(self, start_date: date, embargo_date: date) -> List[Order]:

        if not isinstance(start_date, date) or not isinstance(embargo_date, date):
            raise TypeError("Start date and end date must be datetime.date objects.")

        django_orders: List[Order] = self.order_repo.get_orders_between_dates(
            start_date,
            embargo_date
        )
        return django_orders