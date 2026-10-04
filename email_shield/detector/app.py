from flask import Flask, render_template, request
from flask_cors import CORS
import joblib
from pathlib import Path

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "email_model_real.pkl"
VECTORIZER_PATH = BASE_DIR / "tfidf_vectorizer_real.pkl"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def analyze_threats(subject, message):
    text = (subject + " " + message).lower()

    threats = []

    urgent_words = [
        "steidzami",
        "nekavējoties",
        "nekavējoties rīkojieties",
        "24 stundu",
        "pēc iespējas ātrāk"
    ]

    password_words = [
        "parole",
        "paroli",
        "paroles",
        "lietotājvārds",
        "pieteikšanās dati"
    ]

    account_words = [
        "konta pārbaude",
        "konts",
        "konta",
        "bloķēts",
        "bloķēšana"
    ]

    link_words = [
        "saite",
        "noklikšķiniet",
        "spiediet šeit",
        "atveriet saiti"
    ]

    if any(word in text for word in urgent_words):
        threats.append(
            "Tiek izmantots steidzams aicinājums rīkoties."
        )

    if any(word in text for word in password_words):
        threats.append(
            "Tiek pieprasīta parole vai cita piekļuves informācija."
        )

    if any(word in text for word in account_words):
        threats.append(
            "Ziņojumā ir minēta konta pārbaude vai piekļuves ierobežošana."
        )

    if any(word in text for word in link_words):
        threats.append(
            "Ziņojumā ir aicinājums izmantot saiti."
        )

    return threats


@app.route("/analyze", methods=["POST"])
def analyze_api():
    data = request.get_json() or {}

    subject = data.get("subject", "")
    message = data.get("message", "")

    text = subject + " " + message

    text_tfidf = vectorizer.transform([text])

    prediction = model.predict(text_tfidf)[0]

    probabilities = model.predict_proba(text_tfidf)[0]
    classes = model.classes_

    probability_dict = {}

    for class_name, probability in zip(classes, probabilities):
        probability_dict[class_name] = round(
            float(probability * 100),
            2
        )

    threats = analyze_threats(subject, message)

    return {
        "prediction": str(prediction),
        "category": str(prediction),

        "probabilities": probability_dict,

        "phishing_probability": probability_dict.get(
            "phishing", 0
        ),

        "normal_probability": probability_dict.get(
            "normal", 0
        ),

        "spam_probability": probability_dict.get(
            "spam", 0
        ),

        "advertising_probability": probability_dict.get(
            "advertising", 0
        ),

        "threats": threats
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":

        subject = request.form.get("subject", "")
        message = request.form.get("message", "")

        text = subject + " " + message

        text_tfidf = vectorizer.transform([text])

        prediction = model.predict(text_tfidf)[0]

        probabilities = model.predict_proba(text_tfidf)[0]
        classes = model.classes_

        probability_dict = {}

        for class_name, probability in zip(classes, probabilities):
            probability_dict[class_name] = round(
                float(probability * 100),
                2
            )

        threats = analyze_threats(subject, message)

        result = {
            "prediction": str(prediction),
            "probabilities": probability_dict,
            "threats": threats
        }

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":

    print("==============================")
    print("Latvian Email Security")
    print("==============================")
    print()
    print("Serveris darbojas:")
    print("http://127.0.0.1:5000")
    print()
    print("Kategorijas:")
    print(model.classes_)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )