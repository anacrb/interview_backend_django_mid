from abc import ABC, abstractmethod
from datetime import date
from typing import List

from interview.order.models import Order


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def get_orders_between_dates(self, start_date: date, embargo_date: date) -> List[Order]:
        pass
