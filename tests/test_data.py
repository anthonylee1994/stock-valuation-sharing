import unittest

from stock_valuation.data import resolve_ticker


class DataTests(unittest.TestCase):
    def test_resolve_ticker_is_case_insensitive(self) -> None:
        self.assertEqual(resolve_ticker("goog"), "GOOG")


if __name__ == "__main__":
    unittest.main()
