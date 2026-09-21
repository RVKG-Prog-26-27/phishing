import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import joblib


# ---------------------------------------------------------
# Nosakām projekta mapi
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


print("=" * 60)
print("MĀCĪŠANĀS DATU SAGATAVOŠANA")
print("=" * 60)


# ---------------------------------------------------------
# Ielādējam paplašināto datu kopumu
# ---------------------------------------------------------

data_file = BASE_DIR / "latvian_emails_extended.csv"

data = pd.read_csv(data_file)


# ---------------------------------------------------------
# Pārbaudām datu kopumu
# ---------------------------------------------------------

print(f"\nKopējais e-pastu skaits: {len(data)}")

print("\nE-pastu sadalījums:")
print(data["label"].value_counts())

print("\nIzmantotās kolonnas:")
print(data.columns.tolist())


# ---------------------------------------------------------
# Apvienojam e-pasta tēmu un tekstu
# ---------------------------------------------------------

data["text"] = (
    data["subject"].fillna("") + " " +
    data["message"].fillna("")
)


# X — e-pasta teksts
# y — e-pasta klasifikācija

X = data["text"]
y = data["label"]


# ---------------------------------------------------------
# Sadalām datus mācību un testa daļā
# ---------------------------------------------------------

print("\nDatu sadalīšana mācību un testa daļā...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print(f"\nMācību dati: {len(X_train)}")
print(f"Testa dati: {len(X_test)}")


# ---------------------------------------------------------
# TF-IDF vektorizācija
# ---------------------------------------------------------

print("\nTF-IDF vektorizācija...")

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True
)


X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


print("Teksts pārveidots skaitliskā formā.")


# ---------------------------------------------------------
# Izveidojam un apmācām ML modeli
# ---------------------------------------------------------

print("\nMākslīgā intelekta modeļa apmācība...")

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)


model.fit(
    X_train_tfidf,
    y_train
)


print("Modeļa apmācība pabeigta!")


# ---------------------------------------------------------
# Veicam prognozes
# ---------------------------------------------------------

print("\nTestējam modeli...")

y_pred = model.predict(X_test_tfidf)


# ---------------------------------------------------------
# Aprēķinām modeļa precizitāti
# ---------------------------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)


# ---------------------------------------------------------
# Parādām rezultātus
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("MODEĻA REZULTĀTI")
print("=" * 60)


print(
    f"\nPrecizitāte (Accuracy): {accuracy:.2%}"
)


print("\nDetalizēts klasifikācijas pārskats:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Normāls",
            "Pikšķerēšana"
        ]
    )
)


print("\nKļūdu matrica (Confusion Matrix):")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ---------------------------------------------------------
# Saglabājam modeli un TF-IDF vektorizatoru
# ---------------------------------------------------------

model_file = BASE_DIR / "phishing_model.pkl"
vectorizer_file = BASE_DIR / "tfidf_vectorizer.pkl"


joblib.dump(
    model,
    model_file
)


joblib.dump(
    vectorizer,
    vectorizer_file
)


# ---------------------------------------------------------
# Paziņojums par saglabāšanu
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("MODEĻI SAGLABĀTI")
print("=" * 60)

print(f"\n{model_file.name}")
print(f"{vectorizer_file.name}")

print("\nApmācība veiksmīgi pabeigta!")