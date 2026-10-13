import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\Nas Graphy\Downloads\Data visdualtion\Week 1\penguins.csv")

print(df.isnull().sum())

# 2 rows have all four measurements missing, so remove them for measurement plots
df_measurements = df.dropna(
    subset=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    how="all"
)

# 11 rows have missing sex, so remove them only for the sex comparison
df_sex = df.dropna(subset=["sex"])

sns.set_theme(style="whitegrid")

# 1. Body mass distribution
plt.figure(figsize=(8, 5))
sns.histplot(df_measurements["body_mass_g"], kde=True)
plt.title("Distribution of Body Mass")
plt.xlabel("Body Mass (g)")
plt.ylabel("Count")
plt.figtext(
    0.5, 0.01,
    "2 penguins missing all four measurements were excluded.",
    ha="center"
)
plt.tight_layout()
plt.show()

# 2. Body mass distribution by species
plt.figure(figsize=(8, 5))
sns.histplot(
    data=df_measurements,
    x="body_mass_g",
    hue="species",
    kde=True,
    element="step"
)
plt.title("Body Mass Distribution by Species")
plt.xlabel("Body Mass (g)")
plt.ylabel("Count")
plt.figtext(
    0.5, 0.01,
    "2 penguins missing all four measurements were excluded.",
    ha="center"
)
plt.tight_layout()
plt.show()

# 3. Bill length and bill depth
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=df_measurements,
    x="bill_depth_mm",
    y="bill_length_mm",
    hue="species"
)
plt.title("Bill Length vs Bill Depth")
plt.xlabel("Bill Depth (mm)")
plt.ylabel("Bill Length (mm)")
plt.figtext(
    0.5, 0.01,
    "2 penguins missing all four measurements were excluded.",
    ha="center"
)
plt.tight_layout()
plt.show()

# 4. Average body mass by species and sex
average_mass = (
    df_sex.groupby(["species", "sex"])["body_mass_g"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(8, 5))
sns.barplot(
    data=average_mass,
    x="species",
    y="body_mass_g",
    hue="sex"
)
plt.title("Average Body Mass by Species and Sex")
plt.xlabel("Species")
plt.ylabel("Average Body Mass (g)")
plt.figtext(
    0.5, 0.01,
    "11 penguins with missing sex were excluded.",
    ha="center"
)
plt.tight_layout()
plt.show()

print("\nAverage body mass by species and sex:")
print(average_mass)

print("\nCorrelation between bill length and bill depth:")

print(
    "All penguins:",
    df_measurements["bill_length_mm"].corr(
        df_measurements["bill_depth_mm"]
    )
)

for species, group in df_measurements.groupby("species"):
    print(
        species + ":",
        group["bill_length_mm"].corr(group["bill_depth_mm"])
    )
