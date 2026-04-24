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
avg = df.groupby("year")["cashflow"].mean()

plt.style.use("fivethirtyeight")
plt.figure(figsize=(10,5))

for run_id, run_data in df.groupby("run"):
    plt.plot(run_data["year"], run_data["cashflow"], alpha=0.05)

plt.plot(avg.index, avg.values, linewidth=3)

plt.xlabel("Year")
plt.ylabel("Cashflow")
plt.title("Cashflow per Run")

plt.figure()

df["cashflow"].hist(bins=50)

plt.xlabel("Cashflow")
plt.ylabel("Frequency")
plt.title("Cashflow Distribution")

plt.show()