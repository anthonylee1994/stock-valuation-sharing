"""
生成博通 (AVGO) 彩虹估值圖
"""

from rainbow_chart import create_rainbow_chart

avgo_eps = {
    2021: 27.45,
    2022: 33.20,
    2023: 41.42,
    2024: 15.41,  # VMware 併購影響
    2025: 59.69,
    2026: 9.00,   # 預估
    2027: 16.55,  # 預估
}

avgo_pe_bands = {
    '嚴重高估': 45,
    '高估': 40.0,
    '合理偏高': 33,
    '合理估值': 28.5,
    '合理偏低': 23,
    '低估': 18.0,
    '嚴重低估': 14,
}

create_rainbow_chart(
    ticker_symbol='AVGO',
    eps_by_year=avgo_eps,
    pe_bands=avgo_pe_bands,
)
