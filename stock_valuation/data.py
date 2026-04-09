"""
估值資料載入與路徑管理。
"""

from dataclasses import dataclass
import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
VALUATION_DIR = DATA_DIR / "valuation"
RAINBOW_CHARTS_DIR = DATA_DIR / "rainbow_charts"
REFERENCES_DIR = DATA_DIR / "references"
SCHEMA_PATH = VALUATION_DIR / "schema.json"


@dataclass(frozen=True)
class ValuationData:
    ticker: str
    eps_by_year: dict[int, float]
    pe_bands: dict[str, float]
    raw: dict
    source_path: Path


def list_available_tickers() -> list[str]:
    """列出所有可用嘅估值資料代號。"""
    return sorted(path.stem for path in VALUATION_DIR.glob("*.json") if path.name != "schema.json")


def resolve_ticker(ticker_symbol: str) -> str:
    """將輸入 ticker 對應到實際檔名。"""
    available = {ticker.upper(): ticker for ticker in list_available_tickers()}
    normalized = ticker_symbol.upper()

    if normalized not in available:
        available_list = ", ".join(list_available_tickers())
        raise FileNotFoundError(f"找不到 {ticker_symbol} 嘅估值資料。可用代號: {available_list}")

    return available[normalized]


def load_valuation_data(ticker_symbol: str) -> ValuationData:
    """載入單一股票估值 JSON。"""
    resolved_ticker = resolve_ticker(ticker_symbol)
    source_path = VALUATION_DIR / f"{resolved_ticker}.json"

    with source_path.open(encoding="utf-8") as file:
        raw_data = json.load(file)

    eps_by_year = {int(year): eps for year, eps in raw_data["eps"].items()}

    return ValuationData(
        ticker=raw_data["ticker"],
        eps_by_year=eps_by_year,
        pe_bands=raw_data["pe_bands"],
        raw=raw_data,
        source_path=source_path,
    )


def build_chart_output_path(ticker_symbol: str, output_dir: Path | None = None) -> Path:
    """建立圖表輸出路徑。"""
    target_dir = output_dir or RAINBOW_CHARTS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    resolved_ticker = resolve_ticker(ticker_symbol)
    return target_dir / f"{resolved_ticker}.png"
