import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL = BASE_DIR / "email_model_real.pkl"
VECTORIZER = BASE_DIR / "tfidf_vectorizer_real.pkl"

print("Загружаю модель, обученную на реальных письмах...")

model = joblib.load(MODEL)
vectorizer = joblib.load(VECTORIZER)

print("Модель загружена!")
print("Классы:", list(model.classes_))
print()

sender = input("Sender: ")
subject = input("Subject: ")
message = input("Message: ")

text = f"{sender} {subject} {message}"

text_tfidf = vectorizer.transform([text])

prediction = model.predict(text_tfidf)[0]
probabilities = model.predict_proba(text_tfidf)[0]

print("\n==============================")
print("LATVIAN EMAIL SECURITY")
print("==============================")

print(f"\nPrognoze: {prediction}")

print("\nVarbūtības:")

for class_name, probability in zip(model.classes_, probabilities):
    print(f"{class_name:12} {probability * 100:.2f}%")