"""
股票彩虹估值圖生成器
製作專業嘅 TradingView 風格圖表，包含動態估值區間
可以應用於任何有歷史每股盈利數據嘅股票
"""

from datetime import datetime, timedelta
from typing import TypeAlias

import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.axes import Axes
from matplotlib.figure import Figure

EPSByYear: TypeAlias = dict[int, float]
PEBands: TypeAlias = dict[str, float]
PriceBands: TypeAlias = dict[str, list[float]]

FONT_SANS_SERIF = [
    "Arial Unicode MS",
    "PingFang HK",
    "Heiti TC",
    "Microsoft YaHei",
    "SimHei",
]
CHART_BACKGROUND = "#131722"
PANEL_BACKGROUND = "#1E222D"
TEXT_COLOR = "#D1D4DC"
GRID_COLOR = "#363A45"
PRICE_LINE_COLOR = "#FFFFFF"
CURRENT_PRICE_COLOR = "#FFA500"


# 設定中文字體
plt.rcParams["font.sans-serif"] = FONT_SANS_SERIF
plt.rcParams["axes.unicode_minus"] = False  # 修正負號顯示


def fetch_stock_data(ticker_symbol: str, start_date: str, end_date: str):
    """獲取股票歷史數據"""
    print(f"📊 正在獲取 {ticker_symbol} 歷史數據...")
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(start=start_date, end=end_date)

    if df.empty:
        print("❌ 無法獲取數據。")
        return None

    print(f"✅ 已獲取 {len(df)} 個數據點")
    return df


def validate_inputs(eps_by_year: EPSByYear, pe_bands: PEBands) -> None:
    """確認必要輸入完整。"""
    if not eps_by_year:
        raise ValueError("eps_by_year 不能為空")
    if not pe_bands:
        raise ValueError("pe_bands 不能為空")


def get_default_date_range() -> tuple[str, str]:
    """回傳預設查詢區間（最近五年）。"""
    now = datetime.now()
    start_date = (now - timedelta(days=365 * 5)).strftime("%Y-%m-%d")
    end_date = now.strftime("%Y-%m-%d")
    return start_date, end_date


def get_eps_for_date(date, eps_by_year: EPSByYear) -> float:
    """獲取指定日期嘅每股盈利，喺年份之間進行插值"""
    years = sorted(eps_by_year)
    year = date.year

    if year in eps_by_year:
        return eps_by_year[year]
    if year <= years[0]:
        return eps_by_year[years[0]]
    if year >= years[-1]:
        return eps_by_year[years[-1]]

    for start_year, end_year in zip(years, years[1:]):
        if start_year <= year <= end_year:
            start_eps = eps_by_year[start_year]
            end_eps = eps_by_year[end_year]
            progress = (year - start_year) / (end_year - start_year)
            return start_eps + (end_eps - start_eps) * progress

    raise ValueError(f"No EPS data found for year {year}")


def calculate_price_bands(
    df,
    eps_by_year: EPSByYear,
    pe_bands: PEBands,
) -> PriceBands:
    """為每個日期計算動態價格區間"""
    return {
        label: [get_eps_for_date(date, eps_by_year) * pe for date in df.index]
        for label, pe in pe_bands.items()
    }


def get_band_colors() -> dict[str, str]:
    """返回彩虹顏色映射"""
    return {
        "嚴重高估": "#8B0000",
        "高估": "#FF4500",
        "合理偏高": "#FFD700",
        "合理估值": "#00FF00",
        "合理偏低": "#00CED1",
        "低估": "#1E90FF",
        "嚴重低估": "#8A2BE2",
    }


def setup_chart() -> tuple[Figure, Axes]:
    """建立同設定圖表"""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(20, 11))
    fig.patch.set_facecolor(CHART_BACKGROUND)
    ax.set_facecolor(CHART_BACKGROUND)
    return fig, ax


def plot_rainbow_bands(
    ax: Axes,
    df,
    price_bands_dynamic: PriceBands,
    pe_bands: PEBands,
    band_colors: dict[str, str],
) -> None:
    """繪製彩虹估值線"""
    for label, prices in price_bands_dynamic.items():
        ax.plot(
            df.index,
            prices,
            color=band_colors[label],
            linestyle="-",
            linewidth=1.5,
            alpha=0.9,
            label=f"{label} (P/E {pe_bands[label]}x)",
            zorder=2,
        )


def plot_stock_price(ax: Axes, df) -> None:
    """繪製股價線"""
    ax.plot(df.index, df["Close"], color=PRICE_LINE_COLOR, linewidth=1, alpha=0.9, zorder=5)


def mark_current_price(ax: Axes, df) -> None:
    """標記同註釋現價"""
    current_price = df["Close"].iloc[-1]
    current_date = df.index[-1]

    ax.plot(
        current_date,
        current_price,
        "o",
        color=CURRENT_PRICE_COLOR,
        markersize=14,
        markeredgewidth=3,
        markeredgecolor="white",
        zorder=20,
    )

    ax.annotate(
        f"現價: ${current_price:.2f}",
        xy=(current_date, current_price),
        xytext=(-80, 30),
        textcoords="offset points",
        fontsize=12,
        fontweight="bold",
        color=CURRENT_PRICE_COLOR,
        bbox=dict(
            boxstyle="round,pad=0.6",
            facecolor=PANEL_BACKGROUND,
            edgecolor=CURRENT_PRICE_COLOR,
            linewidth=2,
        ),
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="arc3,rad=0.2",
            lw=2,
            color=CURRENT_PRICE_COLOR,
        ),
        zorder=20,
    )


def add_price_labels(
    ax: Axes,
    df,
    price_bands_dynamic: PriceBands,
    band_colors: dict[str, str],
) -> None:
    """喺右邊加上價格標籤"""
    for label, prices in price_bands_dynamic.items():
        price = prices[-1]
        ax.text(
            df.index[-1],
            price,
            f"  ${price:.0f}",
            verticalalignment="center",
            fontsize=9,
            color=band_colors[label],
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor=CHART_BACKGROUND,
                edgecolor=band_colors[label],
                alpha=0.8,
            ),
        )


def calculate_y_limits(df, price_bands_dynamic: PriceBands) -> tuple[float, float]:
    """根據股價與估值線計算 y 軸上下界。"""
    band_min = min(min(prices) for prices in price_bands_dynamic.values())
    band_max = max(max(prices) for prices in price_bands_dynamic.values())
    y_min = min(df["Close"].min(), band_min) * 0.8
    y_max = max(df["Close"].max(), band_max) * 1.1
    return y_min, y_max


def format_chart(
    ax: Axes,
    ticker_symbol: str,
    df,
    price_bands_dynamic: PriceBands,
) -> None:
    """格式化圖表（標籤、標題、網格、圖例、y軸範圍）"""
    ax.set_xlabel("日期", fontsize=13, fontweight="bold", color=TEXT_COLOR)
    ax.set_ylabel("股價 ($)", fontsize=13, fontweight="bold", color=TEXT_COLOR)
    ax.set_title(
        f"{ticker_symbol} 彩虹估值圖\n基於5年平均市盈率及歷史每股盈利",
        fontsize=16,
        fontweight="bold",
        pad=20,
        color=TEXT_COLOR,
    )

    ax.grid(True, alpha=0.15, linestyle="--", linewidth=0.5, color=GRID_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=10)

    legend = ax.legend(
        loc="upper left",
        fontsize=9,
        framealpha=0.9,
        fancybox=True,
        shadow=True,
        ncol=2,
    )
    legend.get_frame().set_facecolor(PANEL_BACKGROUND)
    legend.get_frame().set_edgecolor(GRID_COLOR)

    y_min, y_max = calculate_y_limits(df, price_bands_dynamic)
    ax.set_ylim(y_min, y_max)


def create_rainbow_chart(
    ticker_symbol: str,
    eps_by_year: EPSByYear,
    pe_bands: PEBands,
    start_date: str = None,
    end_date: str = None,
    save_path: str = None,
    dpi: int = 150,
) -> None:
    """
    為股票製作彩虹估值圖

    參數:
        ticker_symbol: 股票代號 (例如: 'GOOG', 'MSFT')
        eps_by_year: 年份 -> 每股盈利嘅字典
        pe_bands: 估值標籤 -> 市盈率倍數嘅字典
        start_date: 歷史數據開始日期
        end_date: 歷史數據結束日期
        save_path: 儲存路徑 (如果唔指定就直接顯示)
        dpi: 圖片解析度 (預設 150)
    """
    validate_inputs(eps_by_year, pe_bands)

    if start_date is None:
        start_date, default_end_date = get_default_date_range()
        end_date = end_date or default_end_date
    elif end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    df = fetch_stock_data(ticker_symbol, start_date, end_date)
    if df is None:
        return

    price_bands_dynamic = calculate_price_bands(df, eps_by_year, pe_bands)
    band_colors = get_band_colors()
    fig, ax = setup_chart()

    plot_rainbow_bands(ax, df, price_bands_dynamic, pe_bands, band_colors)
    plot_stock_price(ax, df)
    mark_current_price(ax, df)
    add_price_labels(ax, df, price_bands_dynamic, band_colors)
    format_chart(ax, ticker_symbol, df, price_bands_dynamic)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches="tight")
        print(f"✅ 圖表已儲存至: {save_path}")
    else:
        plt.show()

    plt.close(fig)
