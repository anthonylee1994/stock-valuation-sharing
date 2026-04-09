"""
命令列入口。
"""

import argparse
from pathlib import Path

from stock_valuation.data import (
    build_chart_output_path,
    list_available_tickers,
    load_valuation_data,
)
from stock_valuation.payback import calculate_pe_for_payback
from stock_valuation.validation import validate_valuation_files


def build_parser() -> argparse.ArgumentParser:
    """建立 CLI 參數解析器。"""
    parser = argparse.ArgumentParser(description="股票估值工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="生成彩虹估值圖")
    generate_parser.add_argument("tickers", nargs="*", help="股票代號，例如 GOOG 或 0700.HK")
    generate_parser.add_argument("--all", action="store_true", help="為所有股票生成圖表")
    generate_parser.add_argument(
        "--save", action="store_true", help="將圖表儲存到 data/rainbow_charts"
    )
    generate_parser.add_argument("--output-dir", type=Path, help="自訂圖表輸出目錄")
    generate_parser.add_argument("--start-date", help="歷史數據開始日期，格式 YYYY-MM-DD")
    generate_parser.add_argument("--end-date", help="歷史數據結束日期，格式 YYYY-MM-DD")
    generate_parser.add_argument("--dpi", type=int, default=150, help="圖片解析度")
    generate_parser.set_defaults(handler=handle_generate)

    validate_parser = subparsers.add_parser("validate", help="驗證估值 JSON")
    validate_parser.set_defaults(handler=handle_validate)

    list_parser = subparsers.add_parser("list", help="列出可用股票代號")
    list_parser.set_defaults(handler=handle_list)

    payback_parser = subparsers.add_parser("payback-pe", help="計算指定回本年期對應嘅 P/E")
    payback_parser.add_argument("growth_rate", type=float, help="盈利增長率，例如 0.1 或 10")
    payback_parser.add_argument("--years", type=int, default=10, help="目標回本年期")
    payback_parser.set_defaults(handler=handle_payback_pe)

    return parser


def resolve_requested_tickers(tickers: list[str], include_all: bool) -> list[str]:
    """整理 CLI 請求嘅股票代號。"""
    if include_all:
        return list_available_tickers()
    if tickers:
        return tickers
    raise ValueError("請提供至少一個 ticker，或者改用 --all。")


def handle_generate(args: argparse.Namespace) -> int:
    """處理圖表生成。"""
    from stock_valuation.chart import create_rainbow_chart

    requested_tickers = resolve_requested_tickers(args.tickers, args.all)

    for ticker_symbol in requested_tickers:
        valuation_data = load_valuation_data(ticker_symbol)
        save_path = None

        if args.save:
            save_path = build_chart_output_path(valuation_data.ticker, args.output_dir)

        create_rainbow_chart(
            ticker_symbol=valuation_data.ticker,
            eps_by_year=valuation_data.eps_by_year,
            pe_bands=valuation_data.pe_bands,
            start_date=args.start_date,
            end_date=args.end_date,
            save_path=str(save_path) if save_path else None,
            dpi=args.dpi,
        )

    return 0


def handle_validate(_: argparse.Namespace) -> int:
    """處理 schema 驗證。"""
    return 0 if validate_valuation_files() else 1


def handle_list(_: argparse.Namespace) -> int:
    """列出可用 ticker。"""
    for ticker in list_available_tickers():
        print(ticker)
    return 0


def normalize_growth_rate(growth_rate: float) -> float:
    """支援傳入小數或百分比格式。"""
    if growth_rate > 1:
        return growth_rate / 100
    return growth_rate


def handle_payback_pe(args: argparse.Namespace) -> int:
    """計算指定增長率下嘅回本 P/E。"""
    growth_rate = normalize_growth_rate(args.growth_rate)
    pe_ratio = calculate_pe_for_payback(growth_rate=growth_rate, years=args.years)

    print(f"增長率 = {growth_rate * 100:.2f}%")
    print(f"回本年期 = {args.years}")
    print(f"合理 P/E = {pe_ratio:.2f}")
    return 0


def main() -> int:
    """CLI 主入口。"""
    parser = build_parser()
    args = parser.parse_args()

    try:
        return args.handler(args)
    except (FileNotFoundError, ValueError) as error:
        parser.exit(status=1, message=f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
