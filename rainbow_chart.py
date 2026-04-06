"""
Stock Rainbow Valuation Chart Generator
Creates professional TradingView-style charts with candlesticks and dynamic valuation bands
Can be applied to any stock with historical EPS data
"""

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import yfinance as yf
from typing import Dict

# Set Chinese font for matplotlib
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC', 'Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False  # Fix minus sign display


def create_rainbow_chart(
    ticker_symbol: str,
    eps_by_year: Dict[int, float],
    pe_bands: Dict[str, float],
    start_date: str = (datetime.now() - timedelta(days=365*5)).strftime("%Y-%m-%d"),
    end_date: str = datetime.now().strftime("%Y-%m-%d")
):
    """
    Create a rainbow valuation chart for a stock

    Args:
        ticker_symbol: Stock ticker (e.g., 'GOOG', 'MSFT')
        eps_by_year: Dictionary of year -> EPS values
        pe_bands: Dictionary of valuation label -> P/E multiple
        start_date: Start date for historical data
        end_date: End date for historical data
        output_path: Path to save the chart (optional)
    """

    # Fetch historical data
    print(f"📊 Fetching {ticker_symbol} historical data...")
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(start=start_date, end=end_date)

    if df.empty:
        print("❌ No data fetched.")
        return

    print(f"✅ Fetched {len(df)} data points")

    # Helper function to get EPS for any date
    def get_eps_for_date(date):
        """Get EPS for a given date, interpolating between years"""
        year = date.year
        if year in eps_by_year:
            return eps_by_year[year]
        elif year < min(eps_by_year.keys()):
            return eps_by_year[min(eps_by_year.keys())]
        elif year > max(eps_by_year.keys()):
            return eps_by_year[max(eps_by_year.keys())]
        else:
            # Linear interpolation between years
            years = sorted(eps_by_year.keys())
            for i in range(len(years) - 1):
                if years[i] <= year <= years[i+1]:
                    y1, y2 = years[i], years[i+1]
                    eps1, eps2 = eps_by_year[y1], eps_by_year[y2]
                    progress = (year - y1) / (y2 - y1)
                    return eps1 + (eps2 - eps1) * progress
            return eps_by_year[year]

    # Calculate dynamic price bands for each date
    price_bands_dynamic = {}
    for label, pe in pe_bands.items():
        price_bands_dynamic[label] = [get_eps_for_date(date) * pe for date in df.index]

    # Rainbow colors
    band_colors = {
        '嚴重高估': '#8B0000',
        '高估': '#FF4500',
        '合理偏高': '#FFD700',
        '合理估值': '#00FF00',
        '合理偏低': '#00CED1',
        '低估': '#1E90FF',
        '嚴重低估': '#8A2BE2',
    }

    # Create figure
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(20, 11))
    fig.patch.set_facecolor('#131722')
    ax.set_facecolor('#131722')

    # Plot rainbow lines
    line_widths = [3, 3, 3, 3.5, 3, 3, 3]  # Make Fair Value line thicker
    for idx, (label, prices) in enumerate(price_bands_dynamic.items()):
        ax.plot(df.index, prices, color=band_colors[label], linestyle='-',
                linewidth=line_widths[idx], alpha=0.9,
                label=f'{label} (P/E {pe_bands[label]}x)', zorder=2)

    # Plot candlesticks
    def plot_candlestick(ax, df):
        """Plot candlestick chart"""
        df_weekly = df.resample('W').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()

        width = 0.6
        width2 = 0.05

        up = df_weekly[df_weekly.Close >= df_weekly.Open]
        down = df_weekly[df_weekly.Close < df_weekly.Open]

        # Up candles (green)
        ax.bar(up.index, up.Close - up.Open, width, bottom=up.Open,
               color='#26a69a', edgecolor='#26a69a', alpha=0.8, zorder=5)
        ax.bar(up.index, up.High - up.Close, width2, bottom=up.Close,
               color='#26a69a', edgecolor='#26a69a', alpha=0.8, zorder=5)
        ax.bar(up.index, up.Open - up.Low, width2, bottom=up.Low,
               color='#26a69a', edgecolor='#26a69a', alpha=0.8, zorder=5)

        # Down candles (red)
        ax.bar(down.index, down.Open - down.Close, width, bottom=down.Close,
               color='#ef5350', edgecolor='#ef5350', alpha=0.8, zorder=5)
        ax.bar(down.index, down.High - down.Open, width2, bottom=down.Open,
               color='#ef5350', edgecolor='#ef5350', alpha=0.8, zorder=5)
        ax.bar(down.index, down.Close - down.Low, width2, bottom=down.Low,
               color='#ef5350', edgecolor='#ef5350', alpha=0.8, zorder=5)

    plot_candlestick(ax, df)

    # Mark current price
    current_price = df['Close'].iloc[-1]
    current_date = df.index[-1]
    ax.plot(current_date, current_price, 'o', color='#FFA500', markersize=14,
            markeredgewidth=3, markeredgecolor='white', zorder=20)

    ax.annotate(f'現價: ${current_price:.2f}',
                xy=(current_date, current_price),
                xytext=(-80, 30), textcoords='offset points',
                fontsize=12, fontweight='bold', color='#FFA500',
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#1E222D',
                         edgecolor='#FFA500', linewidth=2),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2',
                               lw=2, color='#FFA500'),
                zorder=20)

    # Add price labels on the right
    for label, prices in price_bands_dynamic.items():
        price = prices[-1]
        ax.text(df.index[-1], price, f'  ${price:.0f}',
                verticalalignment='center', fontsize=9, color=band_colors[label],
                fontweight='bold', bbox=dict(boxstyle='round,pad=0.3',
                facecolor='#131722', edgecolor=band_colors[label], alpha=0.8))

    # Formatting
    ax.set_xlabel('日期', fontsize=13, fontweight='bold', color='#D1D4DC')
    ax.set_ylabel('股價 ($)', fontsize=13, fontweight='bold', color='#D1D4DC')
    ax.set_title(f'{ticker_symbol} 彩虹估值圖\n基於5年平均市盈率及歷史每股盈利',
                 fontsize=16, fontweight='bold', pad=20, color='#D1D4DC')

    ax.grid(True, alpha=0.15, linestyle='--', linewidth=0.5, color='#363A45')
    ax.tick_params(colors='#D1D4DC', labelsize=10)

    # Legend
    legend = ax.legend(loc='upper left', fontsize=9, framealpha=0.9,
                       fancybox=True, shadow=True, ncol=2)
    legend.get_frame().set_facecolor('#1E222D')
    legend.get_frame().set_edgecolor('#363A45')

    # Set y-axis limits
    y_min = min(df['Close'].min(), min([min(prices) for prices in price_bands_dynamic.values()])) * 0.8
    y_max = max([max(prices) for prices in price_bands_dynamic.values()]) * 1.1
    ax.set_ylim(y_min, y_max)

    plt.tight_layout()
    plt.show()

