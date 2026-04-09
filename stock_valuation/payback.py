"""
回本年期對應 P/E 計算。
"""


def calculate_pe_for_payback(growth_rate: float, years: int = 10) -> float:
    """計算指定盈利增長率下，喺目標年期回本所對應嘅 P/E。"""
    if years <= 0:
        raise ValueError("years 必須大於 0")

    if growth_rate <= -1:
        raise ValueError("growth_rate 必須大於 -1")

    if growth_rate == 0:
        return float(years)

    pe_ratio = (1 + growth_rate) * ((1 + growth_rate) ** years - 1) / growth_rate
    return round(pe_ratio, 2)
