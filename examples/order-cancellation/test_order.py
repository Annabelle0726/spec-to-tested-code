import unittest
from dataclasses import replace

from order import Order, cancel_order


class CancellationTests(unittest.TestCase):
    def test_s1_owner_cancels_unshipped_order(self):
        order = Order("order-101", "alice", "unshipped")
        self.assertTrue(cancel_order(order, "alice"))
        self.assertEqual(order, Order("order-101", "alice", "cancelled"))

    def test_s2_another_owner_and_order(self):
        order = Order("order-209", "chen", "unshipped")
        self.assertTrue(cancel_order(order, "chen"))
        self.assertEqual(order, Order("order-209", "chen", "cancelled"))

    def test_s3_non_owner_is_rejected_without_changes(self):
        order = Order("order-101", "alice", "unshipped")
        original = replace(order)
        self.assertFalse(cancel_order(order, "bob"))
        self.assertEqual(order, original)

    def test_s4_shipped_order_is_rejected_without_changes(self):
        order = Order("order-101", "alice", "shipped")
        original = replace(order)
        self.assertFalse(cancel_order(order, "alice"))
        self.assertEqual(order, original)


if __name__ == "__main__":
    unittest.main()
