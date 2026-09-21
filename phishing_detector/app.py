from flask import Flask, render_template, request
from flask_cors import CORS
import joblib
from pathlib import Path


app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent

# Ielādējam apmācīto modeli un TF-IDF vektorizatoru
model = joblib.load(BASE_DIR / "phishing_model.pkl")
vectorizer = joblib.load(BASE_DIR / "tfidf_vectorizer.pkl")


def analyze_threats(subject, message):
    """
    Papildu noteikumu analīze, lai paskaidrotu
    iespējamās draudu pazīmes.
    """

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


# ==========================================
# API Chrome Extension
# ==========================================

@app.route("/analyze", methods=["POST"])
def analyze_api():

    data = request.get_json()

    subject = data.get("subject", "")
    message = data.get("message", "")

    text = subject + " " + message

    # Pārveidojam tekstu TF-IDF formātā
    text_tfidf = vectorizer.transform([text])

    # Iegūstam prognozi
    prediction = model.predict(text_tfidf)[0]

    # Iegūstam modeļa varbūtības
    probabilities = model.predict_proba(text_tfidf)[0]
    classes = model.classes_

    phishing_probability = float(
        probabilities[list(classes).index("phishing")] * 100
    )

    normal_probability = float(
        probabilities[list(classes).index("normal")] * 100
    )

    # Papildu draudu pazīmes
    threats = analyze_threats(subject, message)

    # Nosakām, vai vēstule ir bīstama
    dangerous = "JĀ" if phishing_probability >= 50 else "NĒ"

    return {
        "prediction": str(prediction),
        "phishing_probability": round(phishing_probability, 2),
        "normal_probability": round(normal_probability, 2),
        "dangerous": dangerous,
        "threats": threats
    }


# ==========================================
# Flask mājaslapa
# ==========================================

@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        subject = request.form.get("subject", "")
        message = request.form.get("message", "")

        text = subject + " " + message

        # Pārveidojam tekstu TF-IDF formātā
        text_tfidf = vectorizer.transform([text])

        # Prognoze
        prediction = model.predict(text_tfidf)[0]

        # Modeļa varbūtības
        probabilities = model.predict_proba(text_tfidf)[0]
        classes = model.classes_

        phishing_probability = float(
            probabilities[list(classes).index("phishing")] * 100
        )

        normal_probability = float(
            probabilities[list(classes).index("normal")] * 100
        )

        # Draudu pazīmes
        threats = analyze_threats(subject, message)

        result = {
            "prediction": str(prediction),
            "phishing_probability": round(
                phishing_probability, 2
            ),
            "normal_probability": round(
                normal_probability, 2
            ),
            "threats": threats
        }

    return render_template(
        "index.html",
        result=result
    )


# ==========================================
# Flask palaišana
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)