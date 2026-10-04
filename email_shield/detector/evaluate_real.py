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

BASE_DIR = Path(__file__).resolve().parent
DATASET = BASE_DIR / "real_latvian_emails_fixed.csv"

print("Загружаю реальные письма...")

df = pd.read_csv(
    DATASET,
    encoding="utf-8-sig",
    skipinitialspace=True
)

required_columns = ["sender", "subject", "message", "label"]

for column in required_columns:
    if column not in df.columns:
        print(f"ОШИБКА: отсутствует колонка {column}")
        exit()


for column in ["sender", "subject", "message"]:
    df[column] = df[column].fillna("").astype(str)


valid_labels = [
    "normal",
    "phishing",
    "spam",
    "advertising"
]

df = df[df["label"].isin(valid_labels)].copy()

print("\n==============================")
print("ДАННЫЕ")
print("==============================")

print("Всего писем:", len(df))

print("\nРаспределение классов:")
print(df["label"].value_counts())


df["text"] = (
    df["sender"] + " " +
    df["subject"] + " " +
    df["message"]
)

X = df["text"]
y = df["label"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n==============================")
print("РАЗДЕЛЕНИЕ")
print("==============================")

print("Обучение:", len(X_train))
print("Тест:", len(X_test))


print("\nСоздаю TF-IDF...")

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    min_df=1,
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("Размер обучающего TF-IDF:", X_train_tfidf.shape)
print("Размер тестового TF-IDF:", X_test_tfidf.shape)

# Обучение
print("\nОбучаю Logistic Regression...")

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_tfidf, y_train)


y_pred = model.predict(X_test_tfidf)


accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("РЕЗУЛЬТАТЫ")
print("==============================")

print(f"\nAccuracy: {accuracy * 100:.2f}%")


print("\nClassification Report:")
print("--------------------------------")

print(
    classification_report(
        y_test,
        y_pred,
        labels=model.classes_,
        zero_division=0
    )
)


print("\nConfusion Matrix:")
print("--------------------------------")

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=model.classes_
)

print("Классы:")
print(list(model.classes_))
print()

print(cm)


print("\n==============================")
print("ОШИБКИ МОДЕЛИ")
print("==============================")

errors = 0

for text, real, predicted in zip(X_test, y_test, y_pred):

    if real != predicted:

        errors += 1

        print("\n--------------------------------")
        print("Правильно:", real)
        print("Модель сказала:", predicted)
        print("Текст:")
        print(text[:500])

if errors == 0:
    print("\nОшибок на тестовой выборке нет! 🎉")
else:
    print(f"\nВсего ошибок: {errors}")