"""
Generate AVGO rainbow valuation chart
"""

from rainbow_chart import create_rainbow_chart

avgo_eps = {
    2021: 27.45,
    2022: 33.20,
    2023: 41.42,
    2024: 15.41,  # VMware acquisition impact
    2025: 59.69,
    2026: 9.00,   # Estimated
    2027: 16.55,  # Estimated
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
