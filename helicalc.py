import matplotlib.pyplot as plt
import random
import pandas as pd

pd.set_option("display.float_format", "{:,.2f}".format)

runs = 1_000
years = 20

results = []

for run in range(runs):

    loan = 2_000_000
    rate = 0.055 / 12
    n = 15 * 12

    monthly_payment = loan * (rate * (1 + rate)**n) / ((1 + rate)**n - 1)

    for year in range(years):

        flighthours = random.triangular(300, 650, 450)
        revenue = flighthours * 60 * 35

        var_cost = flighthours * random.triangular(900, 1_300, 1_100)
        fixed_cost = random.triangular(120_000, 250_000, 180_000)

        deprecitaion = flighthours * 250

        yearly_payment = 0

        for month in range(12):
            if loan <= 0:
                break

            interest = loan * rate
            principal = monthly_payment - interest

            if principal > loan:
                principal = loan
                payment = interest + principal
            else:
                payment = monthly_payment

            loan -= principal
            loan = max(0, loan)

            yearly_payment += payment

        operating_profit = revenue - var_cost - fixed_cost - deprecitaion
        cashflow = revenue - var_cost - fixed_cost - yearly_payment

        results.append({
            "run" : run,
            "year" : year,
            "cashflow" : cashflow
        })

df = pd.DataFrame(results)

plt.style.use("fivethirtyeight")

df["cashflow"].hist(bins=50)

plt.xlabel("Cashflow")
plt.ylabel("Frequency")
plt.title("Cashflow Distribution")

run_cashflow = df.groupby("run")["cashflow"].sum()
avg = df.groupby("year")["cashflow"].mean()

best_run = run_cashflow.idxmax()
worst_run = run_cashflow.idxmin()

best_data = df[df["run"] == best_run]
worst_data = df[df["run"] == worst_run]

plt.figure(figsize=(10, 5))

plt.plot(best_data["year"], best_data["cashflow"], label="Best Run", linewidth=3)
plt.plot(worst_data["year"], worst_data["cashflow"], label="Worst Run", linewidth=3)
plt.plot(avg.index, avg.values, label="Average", linewidth=3)

plt.xlabel("Year")
plt.ylabel("Cashflow")
plt.title("Best vs Worst Run")
plt.legend()

plt.show()
