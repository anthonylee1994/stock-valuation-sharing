# Stock Valuation Sharing

股票估值分析與彩虹估值圖生成工具

## 功能特點

- 📊 **彩虹估值圖生成器** - 基於歷史市盈率的動態估值區間視覺化
- 🕯️ **陰陽燭圖** - 專業 TradingView 風格的價格走勢圖
- 🌈 **7層估值區間** - 從嚴重低估到嚴重高估的彩虹色帶
- 🇭🇰 **繁體中文支援** - 完整中文化介面
- 📈 **動態估值** - 根據每年 EPS 變化自動調整估值區間

## 快速開始

### 安裝依賴

```bash
uv sync
```

### 生成單一股票圖表

```bash
python GOOG.py      # Google/Alphabet
python MSFT.py      # Microsoft
python TSM.py       # 台積電
python AVGO.py      # Broadcom
python 0700.HK.py   # 騰訊控股
```

### 自訂股票圖表

```python
from rainbow_chart import create_rainbow_chart

# 設定 EPS 數據
my_stock_eps = {
    2021: 10.50,
    2022: 12.30,
    2023: 14.20,
    2024: 16.80,
    2025: 19.50,
    2026: 22.00,  # 預測
    2027: 25.00,  # 預測
}

# 設定 P/E 估值區間
my_pe_bands = {
    '嚴重高估': 35,
    '高估': 30,
    '合理偏高': 25,
    '合理估值': 20,
    '合理偏低': 17,
    '低估': 14,
    '嚴重低估': 10,
}

# 生成圖表
create_rainbow_chart(
    ticker_symbol='AAPL',
    eps_by_year=my_stock_eps,
    pe_bands=my_pe_bands,
)
```

## 專案結構

```
.
├── rainbow_chart.py      # 彩虹估值圖生成器核心模組
├── GOOG.py              # Google 圖表生成腳本
├── MSFT.py              # Microsoft 圖表生成腳本
├── TSM.py               # 台積電圖表生成腳本
├── AVGO.py              # Broadcom 圖表生成腳本
├── 0700.HK.py           # 騰訊控股圖表生成腳本
├── data/
│   ├── stocks/          # 個股分析文件 (MD + PDF)
│   ├── images/          # 生成的圖表
│   ├── models/          # 估值模型與方法論
│   └── summary.md       # 投資組合總結
└── README.md
```

## 已分析股票

| 股票代碼    | 公司名稱        | 當前估值 | 評級                |
| ----------- | --------------- | -------- | ------------------- |
| **GOOG**    | Google/Alphabet | 合理估值 | ⭐⭐⭐ 持有         |
| **MSFT**    | Microsoft       | 嚴重低估 | ⭐⭐⭐⭐⭐ 強力買入 |
| **TSM**     | 台積電          | 合理偏高 | ⭐⭐⭐ 持有         |
| **AVGO**    | Broadcom        | 低估     | ⭐⭐⭐⭐ 買入       |
| **0700.HK** | 騰訊控股        | 合理偏低 | ⭐⭐⭐⭐ 買入       |

詳細分析請參閱 [summary.md](data/summary.md)

## 估值方法論

本工具採用 **5年平均市盈率估值法**：

1. 收集過去5年的歷史 EPS 數據
2. 計算每年的 P/E 高低點
3. 計算5年平均 P/E 區間
4. 結合未來 EPS 預測計算目標價
5. 動態調整估值區間（每年根據 EPS 變化）

詳細方法論請參閱 [估值模型計算步驟](data/models/估值模型計算步驟.md)

## 技術棧

- **Python 3.x**
- **matplotlib** - 圖表繪製
- **yfinance** - 股票數據獲取
- **pandas** - 數據處理
- **numpy** - 數值計算

## 注意事項

⚠️ **免責聲明**：本工具僅供參考，不構成投資建議。投資有風險，請根據自身風險承受能力做出決策。

## 授權

MIT License
