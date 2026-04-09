"""
Stock valuation toolkit.
"""

from stock_valuation.data import (
    REFERENCES_DIR,
    RAINBOW_CHARTS_DIR,
    ROOT_DIR,
    VALUATION_DIR,
    ValuationData,
    list_available_tickers,
    load_valuation_data,
)
from stock_valuation.payback import calculate_pe_for_payback
from stock_valuation.validation import validate_valuation_files


def __getattr__(name: str):
    """Lazy-load chart helpers to avoid importing matplotlib for data-only commands."""
    if name == "create_rainbow_chart":
        from stock_valuation.chart import create_rainbow_chart

        return create_rainbow_chart
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "REFERENCES_DIR",
    "RAINBOW_CHARTS_DIR",
    "ROOT_DIR",
    "VALUATION_DIR",
    "ValuationData",
    "calculate_pe_for_payback",
    "create_rainbow_chart",
    "list_available_tickers",
    "load_valuation_data",
    "validate_valuation_files",
]
