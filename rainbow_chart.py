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
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang HK', 'Heiti TC', 'Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 修正負號顯示


def create_rainbow_chart(
    ticker_symbol: str,
    eps_by_year: Dict[int, float],
    pe_bands: Dict[str, float],
    start_date: str = (datetime.now() - timedelta(days=365*5)).strftime("%Y-%m-%d"),
    end_date: str = datetime.now().strftime("%Y-%m-%d")
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

    # 獲取歷史數據
    print(f"📊 正在獲取 {ticker_symbol} 歷史數據...")
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(start=start_date, end=end_date)

    if df.empty:
        print("❌ 無法獲取數據。")
        return

    print(f"✅ 已獲取 {len(df)} 個數據點")

    # 輔助函數：獲取任何日期嘅每股盈利
    def get_eps_for_date(date):
        """獲取指定日期嘅每股盈利，喺年份之間進行插值"""
        year = date.year
        if year in eps_by_year:
            return eps_by_year[year]
        elif year < min(eps_by_year.keys()):
            return eps_by_year[min(eps_by_year.keys())]
        elif year > max(eps_by_year.keys()):
            return eps_by_year[max(eps_by_year.keys())]
        else:
            # 喺年份之間進行線性插值
            years = sorted(eps_by_year.keys())
            for i in range(len(years) - 1):
                if years[i] <= year <= years[i+1]:
                    y1, y2 = years[i], years[i+1]
                    eps1, eps2 = eps_by_year[y1], eps_by_year[y2]
                    progress = (year - y1) / (y2 - y1)
                    return eps1 + (eps2 - eps1) * progress
            return eps_by_year[year]

    # 為每個日期計算動態價格區間
    price_bands_dynamic = {}
    for label, pe in pe_bands.items():
        price_bands_dynamic[label] = [get_eps_for_date(date) * pe for date in df.index]

    # 彩虹顏色
    band_colors = {
        '嚴重高估': '#8B0000',
        '高估': '#FF4500',
        '合理偏高': '#FFD700',
        '合理估值': '#00FF00',
        '合理偏低': '#00CED1',
        '低估': '#1E90FF',
        '嚴重低估': '#8A2BE2',
    }

    # 建立圖表
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(20, 11))
    fig.patch.set_facecolor('#131722')
    ax.set_facecolor('#131722')

    # 繪製彩虹線
    line_widths = [1.5] * len(band_colors)
    for idx, (label, prices) in enumerate(price_bands_dynamic.items()):
        ax.plot(df.index, prices, color=band_colors[label], linestyle='-',
                linewidth=line_widths[idx], alpha=0.9,
                label=f'{label} (P/E {pe_bands[label]}x)', zorder=2)

    # 繪製股價線
    ax.plot(df.index, df['Close'], color='#FFFFFF', linewidth=1, alpha=0.9, zorder=5)

    # 標記現價
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

    # 喺右邊加上價格標籤
    for label, prices in price_bands_dynamic.items():
        price = prices[-1]
        ax.text(df.index[-1], price, f'  ${price:.0f}',
                verticalalignment='center', fontsize=9, color=band_colors[label],
                fontweight='bold', bbox=dict(boxstyle='round,pad=0.3',
                facecolor='#131722', edgecolor=band_colors[label], alpha=0.8))

    # 格式設定
    ax.set_xlabel('日期', fontsize=13, fontweight='bold', color='#D1D4DC')
    ax.set_ylabel('股價 ($)', fontsize=13, fontweight='bold', color='#D1D4DC')
    ax.set_title(f'{ticker_symbol} 彩虹估值圖\n基於5年平均市盈率及歷史每股盈利',
                 fontsize=16, fontweight='bold', pad=20, color='#D1D4DC')

    ax.grid(True, alpha=0.15, linestyle='--', linewidth=0.5, color='#363A45')
    ax.tick_params(colors='#D1D4DC', labelsize=10)

    # 圖例
    legend = ax.legend(loc='upper left', fontsize=9, framealpha=0.9,
                       fancybox=True, shadow=True, ncol=2)
    legend.get_frame().set_facecolor('#1E222D')
    legend.get_frame().set_edgecolor('#363A45')

    # 設定 y 軸範圍
    y_min = min(df['Close'].min(), min([min(prices) for prices in price_bands_dynamic.values()])) * 0.8
    y_max = max([max(prices) for prices in price_bands_dynamic.values()]) * 1.1
    ax.set_ylim(y_min, y_max)

    plt.tight_layout()
    plt.show()

