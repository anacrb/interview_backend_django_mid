from datetime import date
from typing import List
from abc import ABC, abstractmethod

from interview.inventory.models import Inventory


class InventoryRepositoryInterface(ABC):
    @abstractmethod
    def get_inventories_created_after(self, date_filter: date) -> List[Inventory]:
        pass
