import unittest

from stock_valuation.payback import calculate_pe_for_payback


class PaybackTests(unittest.TestCase):
    def test_rejects_unrealistic_years(self) -> None:
        with self.assertRaises(ValueError):
            calculate_pe_for_payback(0.15, years=1001)

    def test_rejects_unrealistic_growth_rate(self) -> None:
        with self.assertRaises(ValueError):
            calculate_pe_for_payback(10.01, years=10)


if __name__ == "__main__":
    unittest.main()
