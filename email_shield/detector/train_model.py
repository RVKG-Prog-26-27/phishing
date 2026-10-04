import pandas as pd
import joblib

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression




BASE_DIR = Path(__file__).resolve().parent

DATASET = BASE_DIR / "real_latvian_emails_fixed.csv"

MODEL = BASE_DIR / "email_model_real.pkl"

VECTORIZER = BASE_DIR / "tfidf_vectorizer_real.pkl"




print("Загружаю настоящие письма...")

try:

    df = pd.read_csv(
        DATASET,
        encoding="utf-8-sig",
        engine="python"
    )

except Exception as e:

    print("\nОШИБКА ПРИ ЧТЕНИИ CSV:")
    print(e)

    print("\nПроверь файл:")
    print(DATASET)

    exit()




required_columns = [
    "sender",
    "subject",
    "message",
    "label"
]

print("\nКолонки CSV:")

print(
    list(df.columns)
)


for column in required_columns:

    if column not in df.columns:

        print(
            f"\nОШИБКА: отсутствует колонка {column}"
        )

        print(
            "\nНужны колонки:"
        )

        print(
            "sender, subject, message, label"
        )

        exit()




for column in [
    "sender",
    "subject",
    "message"
]:

    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
    )




valid_labels = [
    "normal",
    "phishing",
    "spam",
    "advertising"
]


df = df[
    df["label"].isin(valid_labels)
].copy()




print("\n==============================")
print("НАСТОЯЩИЕ ПИСЬМА")
print("==============================")


print(
    "Всего писем:",
    len(df)
)


print("\nРаспределение классов:")


print(
    df["label"].value_counts()
)




df["text"] = (
    df["sender"] + " " +
    df["subject"] + " " +
    df["message"]
)


X = df["text"]

y = df["label"]




print("\nСоздаю TF-IDF...")


vectorizer = TfidfVectorizer(

    ngram_range=(1, 2),

    min_df=1,

    sublinear_tf=True
)


X_tfidf = vectorizer.fit_transform(
    X
)


print(
    "Размер TF-IDF:",
    X_tfidf.shape
)




print("\nОбучаю Logistic Regression...")


model = LogisticRegression(

    max_iter=2000,

    class_weight="balanced",

    random_state=42
)


model.fit(

    X_tfidf,

    y
)




print("\nСохраняю модель...")


joblib.dump(
    model,
    MODEL
)


joblib.dump(
    vectorizer,
    VECTORIZER
)




print("\n==============================")
print("ГОТОВО!")
print("==============================")


print(
    "\nМодель:",
    MODEL
)


print(
    "TF-IDF:",
    VECTORIZER
)


print("\nКлассы модели:")


print(
    model.classes_
)