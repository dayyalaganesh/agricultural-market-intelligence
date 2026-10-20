
import math
import unittest


class TestDataQualityRules(unittest.TestCase):

    def test_valid_price_is_finite(self):
        price = float("125.50")
        self.assertTrue(math.isfinite(price))

    def test_nan_price_is_invalid(self):
        price = float("nan")
        self.assertFalse(math.isfinite(price))

    def test_infinite_price_is_invalid(self):
        price = float("inf")
        self.assertFalse(math.isfinite(price))

    def test_negative_price_is_detected(self):
        price = -10.0
        self.assertLess(price, 0)

    def test_minimum_price_not_greater_than_maximum(self):
        minimum = 100.0
        maximum = 150.0
        self.assertLessEqual(minimum, maximum)

    def test_modal_price_within_valid_range(self):
        minimum = 100.0
        maximum = 150.0
        modal = 125.0
        self.assertGreaterEqual(modal, minimum)
        self.assertLessEqual(modal, maximum)


if __name__ == "__main__":
    unittest.main()
