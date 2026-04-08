"""
股票彩虹估值圖生成器
製作專業嘅 TradingView 風格圖表，包含動態估值區間
可以應用於任何有歷史每股盈利數據嘅股票
"""

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import yfinance as yf
from typing import Dict

# 設定中文字體
plt.rcParams["font.sans-serif"] = [
    "Arial Unicode MS",
    "PingFang HK",
    "Heiti TC",
    "Microsoft YaHei",
    "SimHei",
]
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


def get_eps_for_date(date, eps_by_year: Dict[int, float]) -> float:
    """獲取指定日期嘅每股盈利，喺年份之間進行插值"""
    year = date.year
    if year in eps_by_year:
        return eps_by_year[year]
    elif year < min(eps_by_year.keys()):
        return eps_by_year[min(eps_by_year.keys())]
    elif year > max(eps_by_year.keys()):
        return eps_by_year[max(eps_by_year.keys())]
    else:
        years = sorted(eps_by_year.keys())
        for i in range(len(years) - 1):
            if years[i] <= year <= years[i + 1]:
                y1, y2 = years[i], years[i + 1]
                eps1, eps2 = eps_by_year[y1], eps_by_year[y2]
                progress = (year - y1) / (y2 - y1)
                return eps1 + (eps2 - eps1) * progress
        raise ValueError(f"No EPS data found for year {year}")


def calculate_price_bands(
    df, eps_by_year: Dict[int, float], pe_bands: Dict[str, float]
) -> Dict[str, list]:
    """為每個日期計算動態價格區間"""
    price_bands_dynamic = {}
    for label, pe in pe_bands.items():
        price_bands_dynamic[label] = [
            get_eps_for_date(date, eps_by_year) * pe for date in df.index
        ]
    return price_bands_dynamic


def get_band_colors() -> Dict[str, str]:
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


def setup_chart():
    """建立同設定圖表"""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(20, 11))
    fig.patch.set_facecolor("#131722")
    ax.set_facecolor("#131722")
    return ax


def plot_rainbow_bands(
    ax,
    df,
    price_bands_dynamic: Dict[str, list],
    pe_bands: Dict[str, float],
    band_colors: Dict[str, str],
):
    """繪製彩虹估值線"""
    line_widths = [1.5] * len(band_colors)
    for idx, (label, prices) in enumerate(price_bands_dynamic.items()):
        ax.plot(
            df.index,
            prices,
            color=band_colors[label],
            linestyle="-",
            linewidth=line_widths[idx],
            alpha=0.9,
            label=f"{label} (P/E {pe_bands[label]}x)",
            zorder=2,
        )


def plot_stock_price(ax, df):
    """繪製股價線"""
    ax.plot(df.index, df["Close"], color="#FFFFFF", linewidth=1, alpha=0.9, zorder=5)


def mark_current_price(ax, df):
    """標記同註釋現價"""
    current_price = df["Close"].iloc[-1]
    current_date = df.index[-1]

    ax.plot(
        current_date,
        current_price,
        "o",
        color="#FFA500",
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
        color="#FFA500",
        bbox=dict(
            boxstyle="round,pad=0.6",
            facecolor="#1E222D",
            edgecolor="#FFA500",
            linewidth=2,
        ),
        arrowprops=dict(
            arrowstyle="->", connectionstyle="arc3,rad=0.2", lw=2, color="#FFA500"
        ),
        zorder=20,
    )


def add_price_labels(
    ax, df, price_bands_dynamic: Dict[str, list], band_colors: Dict[str, str]
):
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
                facecolor="#131722",
                edgecolor=band_colors[label],
                alpha=0.8,
            ),
        )


def format_chart(ax, ticker_symbol: str, df, price_bands_dynamic: Dict[str, list]):
    """格式化圖表（標籤、標題、網格、圖例、y軸範圍）"""
    ax.set_xlabel("日期", fontsize=13, fontweight="bold", color="#D1D4DC")
    ax.set_ylabel("股價 ($)", fontsize=13, fontweight="bold", color="#D1D4DC")
    ax.set_title(
        f"{ticker_symbol} 彩虹估值圖\n基於5年平均市盈率及歷史每股盈利",
        fontsize=16,
        fontweight="bold",
        pad=20,
        color="#D1D4DC",
    )

    ax.grid(True, alpha=0.15, linestyle="--", linewidth=0.5, color="#363A45")
    ax.tick_params(colors="#D1D4DC", labelsize=10)

    legend = ax.legend(
        loc="upper left", fontsize=9, framealpha=0.9, fancybox=True, shadow=True, ncol=2
    )
    legend.get_frame().set_facecolor("#1E222D")
    legend.get_frame().set_edgecolor("#363A45")

    y_min = (
        min(
            df["Close"].min(),
            min([min(prices) for prices in price_bands_dynamic.values()]),
        )
        * 0.8
    )
    y_max = max([max(prices) for prices in price_bands_dynamic.values()]) * 1.1
    ax.set_ylim(y_min, y_max)


def create_rainbow_chart(
    ticker_symbol: str,
    eps_by_year: Dict[int, float],
    pe_bands: Dict[str, float],
    start_date: str = None,
    end_date: str = None,
    save_path: str = None,
):
    """
    為股票製作彩虹估值圖

    參數:
        ticker_symbol: 股票代號 (例如: 'GOOG', 'MSFT')
        eps_by_year: 年份 -> 每股盈利嘅字典
        pe_bands: 估值標籤 -> 市盈率倍數嘅字典
        start_date: 歷史數據開始日期
        end_date: 歷史數據結束日期
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365 * 5)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    df = fetch_stock_data(ticker_symbol, start_date, end_date)
    if df is None:
        return

    price_bands_dynamic = calculate_price_bands(df, eps_by_year, pe_bands)
    band_colors = get_band_colors()
    ax = setup_chart()

    plot_rainbow_bands(ax, df, price_bands_dynamic, pe_bands, band_colors)
    plot_stock_price(ax, df)
    mark_current_price(ax, df)
    add_price_labels(ax, df, price_bands_dynamic, band_colors)
    format_chart(ax, ticker_symbol, df, price_bands_dynamic)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
