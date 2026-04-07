"""
Generate 0700.HK (Tencent) rainbow valuation chart
"""

from rainbow_chart import create_rainbow_chart

# 注意：EPS 以港幣計算，股價亦以港幣計算
# RMB EPS 已按 1.136 匯率換算成 HKD (2026年4月匯率)
tencent_eps = {
    2021: 15.03,  # 13.23 * 1.136
    2022: 12.51,  # 11.01 * 1.136
    2023: 10.38,  # 9.14 * 1.136
    2024: 28.04,  # 24.68 * 1.136
    2025: 32.47,  # 28.58 * 1.136
    2026: 37.49,  # 33.00 * 1.136 (預估)
    2027: 40.90,  # 36.00 * 1.136 (預估)
}

tencent_pe_bands = {
    '嚴重高估': 30,
    '高估': 25.0,
    '合理偏高': 21,
    '合理估值': 18.5,
    '合理偏低': 16,
    '低估': 14.0,
    '嚴重低估': 10,
}

create_rainbow_chart(
    ticker_symbol='0700.HK',
    eps_by_year=tencent_eps,
    pe_bands=tencent_pe_bands,
)
