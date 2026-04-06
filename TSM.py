"""
Generate TSM rainbow valuation chart
"""

from rainbow_chart import create_rainbow_chart

tsm_eps = {
    2021: 4.01,
    2022: 6.23,
    2023: 5.36,
    2024: 6.81,
    2025: 10.64,
    2026: 12.50,  # Estimated
    2027: 15.38,  # Estimated
}

tsm_pe_bands = {
    '嚴重高估': 35,
    '高估': 27.5,
    '合理偏高': 25,
    '合理估值': 22.0,
    '合理偏低': 19,
    '低估': 16.4,
    '嚴重低估': 12,
}

create_rainbow_chart(
    ticker_symbol='TSM',
    eps_by_year=tsm_eps,
    pe_bands=tsm_pe_bands,
)
