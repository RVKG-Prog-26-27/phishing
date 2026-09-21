import joblib
from pathlib import Path


print("=" * 60)
print("LATVIEŠU E-PASTA PIKŠĶERĒŠANAS NOTEIKŠANA")
print("=" * 60)


# Atrodam mapi, kurā atrodas šis Python fails
BASE_DIR = Path(__file__).resolve().parent


# Ielādējam apmācīto modeli un TF-IDF vektorizatoru
model = joblib.load(
    BASE_DIR / "phishing_model.pkl"
)

vectorizer = joblib.load(
    BASE_DIR / "tfidf_vectorizer.pkl"
)


# Lietotājs ievada e-pasta tēmu
subject = input("\nIevadiet e-pasta tēmu: ")

# Lietotājs ievada e-pasta tekstu
message = input("\nIevadiet e-pasta tekstu: ")


# Apvienojam tēmu un ziņas tekstu
text = subject + " " + message


# Pārveidojam tekstu TF-IDF formātā
text_tfidf = vectorizer.transform([text])


# Veicam prognozi
prediction = model.predict(text_tfidf)[0]


# Iegūstam varbūtības
probabilities = model.predict_proba(text_tfidf)[0]

classes = model.classes_

phishing_probability = probabilities[
    list(classes).index("phishing")
]

normal_probability = probabilities[
    list(classes).index("normal")
]


print("\n" + "=" * 60)
print("ANALĪZES REZULTĀTS")
print("=" * 60)


if prediction == "phishing":
    print("\n⚠️ IESPĒJAMA PIKŠĶERĒŠANAS VĒSTULE")
else:
    print("\n✅ VĒSTULE IZSKATĀS DROŠA")

print(f"Pikšķērēšanas vēstules varbūtība: {phishing_probability:.2%}")
print(f"Normālas vēstules varbūtība: {normal_probability:.2%}")

print("\nAnalīze pabeigta.")