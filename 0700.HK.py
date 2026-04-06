"""
Generate 700.HK (Tencent) rainbow valuation chart
"""

from rainbow_chart import create_rainbow_chart

# Note: EPS in RMB, prices in HKD (approximately 1:1 ratio)
tencent_eps = {
    2021: 13.23,
    2022: 11.01,
    2023: 9.14,
    2024: 24.68,
    2025: 28.58,
    2026: 33.00,  # Estimated
    2027: 36.00,  # Estimated
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
