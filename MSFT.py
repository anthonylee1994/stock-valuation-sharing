"""
Generate rainbow valuation charts for multiple stocks
"""

from rainbow_chart import create_rainbow_chart

msft_eps = {
    2021: 8.05,
    2022: 9.65,
    2023: 9.68,
    2024: 11.80,
    2025: 13.64,
    2026: 16.50,  # Estimated
    2027: 20.15,  # Estimated
}

msft_pe_bands = {
    '嚴重高估': 42,
    '高估': 38.7,
    '合理偏高': 35,
    '合理估值': 31.8,
    '合理偏低': 28,
    '低估': 24.9,
    '嚴重低估': 20,
}

create_rainbow_chart(
    ticker_symbol='MSFT',
    eps_by_year=msft_eps,
    pe_bands=msft_pe_bands,
)

