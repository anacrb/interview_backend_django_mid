import unittest
from datetime import date, datetime

from interview.inventory.interfaces import InventoryRepositoryInterface
from interview.inventory.models import Inventory
from interview.inventory.use_cases import GetInventoriesCreatedAfterUseCase


class MockInventoryRepository(InventoryRepositoryInterface):
    def __init__(self, inventories_to_return=None):
        self._inventories = inventories_to_return if inventories_to_return is not None else []

    def get_inventories_created_after(self, date_filter: date):
        return [ inv for inv in self._inventories if inv.created_at.date() >= date_filter ]


class GetInventoriesCreatedAfterUseCaseTest(unittest.TestCase):

    def setUp(self):
        class MockInventory:
            def __init__(self, id, name, created_at):
                self.id = id
                self.name = name
                self.created_at = created_at

        self.mock_inventories_data = [
            MockInventory(1, "Movie A", datetime(2025, 1, 1)),
            MockInventory(2, "Movie B", datetime(2025, 1, 15)),
            MockInventory(3, "Movie C", datetime(2025, 2, 1)),
            MockInventory(4, "Movie D", datetime(2024, 12, 20)),
            MockInventory(5, "Movie E", datetime(2025, 3, 10)),
        ]
        self.mock_repo = MockInventoryRepository(self.mock_inventories_data)
        self.use_case = GetInventoriesCreatedAfterUseCase(self.mock_repo)

    def test_execute_with_valid_date(self):
        # Get inventories created after a specific date
        filter_date = date(2025, 1, 20)
        result = self.use_case.execute(filter_date)
        self.assertEqual(len(result), 2)
        self.assertIn(self.mock_inventories_data[2], result) # Movie C
        self.assertIn(self.mock_inventories_data[4], result) #Movie E

        filter_date_late = date(2025, 6, 1)
        result_late = self.use_case.execute(filter_date_late)
        self.assertEqual(len(result_late), 0)

    def test_execute_with_invalid_date_type(self):
        # Passing a non-date object should raise a ValueError
        with self.assertRaises(ValueError) as cm:
            self.use_case.execute("2025-01-01")
        self.assertIn("date_filter must be a datetime.date object.", str(cm.exception))

    def test_execute_with_exact_date(self):
        # Inventories created on the filter date should be included
        filter_date = date(2025, 1, 1)
        result = self.use_case.execute(filter_date)
        self.assertEqual(len(result), 4) # Movie A, B, C, E
        self.assertIn(self.mock_inventories_data[0], result) # Movie A (created on 2025-01-01)


if __name__ == '__main__':
    unittest.main()