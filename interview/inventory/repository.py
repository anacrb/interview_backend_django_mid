from datetime import date
from typing import List

from interview.inventory.interfaces import InventoryRepositoryInterface
from interview.inventory.models import Inventory


class DjangoInventoryRepository(InventoryRepositoryInterface):
    def get_inventories_created_after(self, date_filter: date) -> List[Inventory]:
        return list(Inventory.objects.filter(created_at__date__gte=date_filter))
