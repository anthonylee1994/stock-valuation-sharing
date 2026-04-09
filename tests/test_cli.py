import argparse
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from stock_valuation.cli import handle_generate
from stock_valuation.data import ValuationData


class CliTests(unittest.TestCase):
    def make_args(self, **overrides) -> argparse.Namespace:
        values = {
            "tickers": ["GOOG"],
            "all": False,
            "save": False,
            "output_dir": None,
            "start_date": None,
            "end_date": None,
            "dpi": 150,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    @patch("stock_valuation.chart.create_rainbow_chart", return_value=False)
    @patch("stock_valuation.cli.load_valuation_data")
    def test_handle_generate_returns_failure_when_chart_generation_fails(
        self,
        mock_load,
        mock_create_chart,
    ) -> None:
        mock_load.return_value = ValuationData(
            ticker="GOOG",
            eps_by_year={2024: 1.0},
            pe_bands={"合理估值": 20.0},
            raw={},
            source_path=Path("data/valuation/GOOG.json"),
        )

        result = handle_generate(self.make_args())

        self.assertEqual(result, 1)
        mock_create_chart.assert_called_once()

    def test_handle_generate_rejects_output_dir_without_save(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            args = self.make_args(output_dir=Path(temp_dir))

            with self.assertRaises(ValueError):
                handle_generate(args)


if __name__ == "__main__":
    unittest.main()
