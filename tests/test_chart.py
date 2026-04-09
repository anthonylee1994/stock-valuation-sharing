import unittest
from unittest.mock import patch

import pandas as pd

from stock_valuation.chart import create_rainbow_chart, get_latest_close_point


class ChartTests(unittest.TestCase):
    def test_get_latest_close_point_uses_last_non_nan_row(self) -> None:
        df = pd.DataFrame(
            {"Close": [100.0, 101.5, float("nan")]},
            index=pd.to_datetime(["2026-04-07", "2026-04-08", "2026-04-09"]),
        )

        current_date, current_price = get_latest_close_point(df)

        self.assertEqual(str(current_date.date()), "2026-04-08")
        self.assertEqual(current_price, 101.5)

    @patch("stock_valuation.chart.fetch_stock_data", return_value=None)
    def test_create_rainbow_chart_returns_false_when_no_data(self, mock_fetch) -> None:
        result = create_rainbow_chart(
            ticker_symbol="GOOG",
            eps_by_year={2024: 1.0},
            pe_bands={"合理估值": 20.0},
            start_date="2026-01-01",
            end_date="2026-04-01",
        )

        self.assertFalse(result)
        mock_fetch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
