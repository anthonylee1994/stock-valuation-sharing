# 批量生成你剛才要的列表 (0% - 100%)
from stock_valuation.payback import calculate_pe_for_payback

print("\n增長率 | 合理 P/E (10年回本)")
print("-" * 25)

for growth_rate in range(0, 101):
    result = calculate_pe_for_payback(growth_rate / 100)
    print(f"{growth_rate:>5}%   |   {result:>5.2f}")
