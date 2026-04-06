"""
Generate GOOG rainbow valuation chart
"""

from rainbow_chart import create_rainbow_chart

goog_eps = {
    2021: 5.61,
    2022: 4.56,
    2023: 5.80,
    2024: 6.91,
    2025: 10.21,
    2026: 11.50,  # Estimated
    2027: 13.41,  # Estimated
}

goog_pe_bands = {
    '嚴重高估': 35,
    '高估': 28.9,
    '合理偏高': 25,
    '合理估值': 22.3,
    '合理偏低': 19,
    '低估': 15.7,
    '嚴重低估': 12,
}

create_rainbow_chart(
    ticker_symbol='GOOG',
    eps_by_year=goog_eps,
    pe_bands=goog_pe_bands,
)
