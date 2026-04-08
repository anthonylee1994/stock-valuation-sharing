"""
生成騰訊 (0700.HK) 彩虹估值圖
"""

import json
from pathlib import Path

from rainbow_chart import create_rainbow_chart

# 讀取 JSON 數據
data_path = Path(__file__).parent / "data" / "valuation" / "0700.HK.json"
with open(data_path) as f:
    data = json.load(f)

# 將 EPS 年份由字串轉換為整數
tencent_eps = {int(year): eps for year, eps in data["eps"].items()}
tencent_pe_bands = data["pe_bands"]

create_rainbow_chart(
    ticker_symbol="0700.HK",
    eps_by_year=tencent_eps,
    pe_bands=tencent_pe_bands,
)
