import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\Nas Graphy\Downloads\Data visdualtion\Week 1\flights.csv")

months = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

df["month_num"] = df["month"].map(months)

df["date"] = pd.to_datetime(
    dict(
        year=df["year"],
        month=df["month_num"],
        day=1
    )
)

df = df.sort_values("date")

sns.set_theme(style="whitegrid")

# 1. Passengers over time
plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["passengers"])
plt.title("Monthly Airline Passengers")
plt.xlabel("Year")
plt.ylabel("Passengers")
plt.tight_layout()
plt.show()

# 2. Seasonal pattern for each year
plt.figure(figsize=(10, 6))

for year, group in df.groupby("year"):
    plt.plot(
        group["month_num"],
        group["passengers"],
        marker="o",
        label=year
    )

plt.xticks(range(1, 13), list(months.keys()), rotation=45)
plt.title("Monthly Seasonal Pattern by Year")
plt.xlabel("Month")
plt.ylabel("Passengers")
plt.legend(title="Year")
plt.tight_layout()
plt.show()

# 3. Average passengers for each month
monthly_average = df.groupby("month_num")["passengers"].mean()

plt.figure(figsize=(9, 5))
plt.bar(
    range(1, 13),
    monthly_average
)
plt.xticks(range(1, 13), list(months.keys()), rotation=45)
plt.title("Average Passengers by Month")
plt.xlabel("Month")
plt.ylabel("Average Passengers")
plt.tight_layout()
plt.show()

print("Busiest month:")
print(months.keys().__iter__().__next__()) if False else print(
    list(months.keys())[monthly_average.values.argmax()]
)

# 4. Compare seasonal variation after adjusting for yearly growth
df["year_average"] = df.groupby("year")["passengers"].transform("mean")
df["relative_passengers"] = (
    df["passengers"] / df["year_average"] * 100
)

plt.figure(figsize=(10, 6))

for year, group in df.groupby("year"):
    plt.plot(
        group["month_num"],
        group["relative_passengers"],
        marker="o",
        label=year
    )

plt.axhline(100, linestyle="--")
plt.xticks(range(1, 13), list(months.keys()), rotation=45)
plt.title("Seasonality Relative to Each Year's Average")
plt.xlabel("Month")
plt.ylabel("Passengers (% of yearly average)")
plt.legend(title="Year")
plt.tight_layout()
plt.show()
