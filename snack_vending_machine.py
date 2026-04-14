import random

runs = 1000
annual_profits = []

quotes = {
    "loss_quote": 0,
    "low_profit_quote": 0,
    "high_profit_quote": 0
}

def percentage_calc(quote, runs):
    percentage = (quote / (runs * 12)) * 100
    return percentage

class TriangularDistribution:
    def __init__(self, min_val, max_val, mode):
        self.min = min_val
        self.max = max_val
        self.mode = mode

    def sample(self):
        return random.triangular(self.min, self.max, self.mode)

class Values:
    def __init__(self):
        # Variable costs
        self.purchase_cost_ratio = TriangularDistribution(0.40, 0.70, 0.55)
        self.selling_price = TriangularDistribution(0.80, 2.00, 3.20)
        self.products_sold = TriangularDistribution(300.0, 900.0, 600.0)

        # Fixed costs
        self.rent = 500.0
        self.maintenance = 150.0
        self.tax_rate = 0.25

value = Values()

for run in range(runs):
    annual_profit = 0.0

    for month in range(12):
        purchase_cost_ratio = value.purchase_cost_ratio.sample()
        selling_price = value.selling_price.sample()
        products_sold = value.products_sold.sample()

        rent = value.rent
        maintenance = value.maintenance
        tax_rate = value.tax_rate

        revenue = selling_price * products_sold
        variable_costs = (selling_price * purchase_cost_ratio) * products_sold
        fixed_costs = rent + maintenance

        profit_before_tax = revenue - variable_costs - fixed_costs
        profit_after_tax = profit_before_tax * (1 - tax_rate)

        annual_profit += profit_after_tax

        if profit_after_tax < 0:
            quotes["loss_quote"] += 1
        elif profit_after_tax < 1000:
            quotes["low_profit_quote"] += 1
        else:
            quotes["high_profit_quote"] += 1

    annual_profits.append(annual_profit)

avg_profit = sum(annual_profits) / len(annual_profits)
min_profit = min(annual_profits)
max_profit = max(annual_profits)

loss_percentage = percentage_calc(quotes["loss_quote"], runs)
break_even_percentage = percentage_calc(quotes["low_profit_quote"], runs)
success_percentage = percentage_calc(quotes["high_profit_quote"], runs)

print("\nProfit overview:")
print(f"Average annual profit: {avg_profit:.2f}€")
print(f"Minimum annual profit: {min_profit:.2f}€")
print(f"Maximum annual profit: {max_profit:.2f}€")

print("\nMonthly quotes:")
print(f"Loss (-): {loss_percentage:.1f}% ({quotes['loss_quote']}x)")
print(f"Low profit (0 to <1000): {break_even_percentage:.1f}% ({quotes['low_profit_quote']}x)")
print(f"High profit (1000+): {success_percentage:.1f}% ({quotes['high_profit_quote']}x)")