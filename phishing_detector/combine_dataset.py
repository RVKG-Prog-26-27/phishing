import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Ielādējam uzlabotos datu kopumus
phishing = pd.read_csv(
    BASE_DIR / "latvian_phishing_extended.csv"
)

normal = pd.read_csv(
    BASE_DIR / "latvian_normal_extended.csv"
)

# Apvienojam abus datu kopumus
data = pd.concat(
    [phishing, normal],
    ignore_index=True
)

# Noņemam dublikātus
data = data.drop_duplicates(
    subset=["subject", "message"]
)

# Sajaucam vēstules
data = data.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# Saglabājam jauno datu kopumu
output_file = BASE_DIR / "latvian_emails_extended.csv"

data.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("=" * 60)
print("PAPLAŠINĀTAIS DATU KOPUMS IR IZVEIDOTS")
print("=" * 60)

print(f"\nKopējais e-pastu skaits: {len(data)}")

print("\nVēstuļu sadalījums:")
print(data["label"].value_counts())

print("\nKolonnas:")
print(data.columns.tolist())

print("\nFails saglabāts:")
print(output_file)

print("\nDatu kopuma izveide pabeigta!")