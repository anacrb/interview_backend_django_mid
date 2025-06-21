from datetime import date
from typing import List

from interview.inventory.interfaces import InventoryRepositoryInterface
from interview.inventory.models import Inventory


class GetInventoriesCreatedAfterUseCase:
    def __init__(self, inventory_repo: InventoryRepositoryInterface):
        self.inventory_repo = inventory_repo

    def execute(self, date_filter: date) -> List[Inventory]:
        """
        Retrieves inventory items created after a specified date.
        """
        if not isinstance(date_filter, date):
            raise ValueError("date_filter must be a datetime.date object.")
        return self.inventory_repo.get_inventories_created_after(date_filter)
