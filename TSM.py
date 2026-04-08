"""
生成台積電 (TSM) 彩虹估值圖
"""

import json
from pathlib import Path

from rainbow_chart import create_rainbow_chart

# 讀取 JSON 數據
data_path = Path(__file__).parent / "data" / "valuation" / "TSM.json"
with open(data_path) as f:
    data = json.load(f)

# 將 EPS 年份由字串轉換為整數
tsm_eps = {int(year): eps for year, eps in data["eps"].items()}
tsm_pe_bands = data["pe_bands"]

create_rainbow_chart(
    ticker_symbol="TSM",
    eps_by_year=tsm_eps,
    pe_bands=tsm_pe_bands,
)
