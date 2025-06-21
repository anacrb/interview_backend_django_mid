from abc import ABC, abstractmethod
from typing import Optional

from interview.order.models import Order


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def deactivate_order(self, order_id: int) -> Optional[Order]:
        pass