import pandas as pd
suspicious_words = {

    "parol": {
        "display": "parole",
        "points": 3,
        "reason": "Vēstule mēģina iegūt lietotāja paroli."
    },

    "steidzam": {
        "display": "steidzamība",
        "points": 2,
        "reason": "Vēstule rada steidzamības sajūtu."
    },

    "nekavē": {
        "display": "steidzama rīcība",
        "points": 2,
        "reason": "Lietotājs tiek mudināts rīkoties nekavējoties."
    },

    "apstiprin": {
        "display": "datu apstiprināšana",
        "points": 3,
        "reason": "Tiek pieprasīts apstiprināt konta vai personas datus."
    },

    "bloķ": {
        "display": "bloķēšana",
        "points": 3,
        "reason": "Vēstulē tiek izmantots drauds par konta bloķēšanu."
    },

    "bank": {
        "display": "banka",
        "points": 3,
        "reason": "Vēstule ir saistīta ar bankas informācijas iegūšanu."
    },

    "kredītkart": {
        "display": "kredītkarte",
        "points": 3,
        "reason": "Vēstule var mēģināt iegūt kredītkartes datus."
    },

    "noklikšķin": {
        "display": "saite",
        "points": 2,
        "reason": "Lietotājs tiek aicināts noklikšķināt uz saites."
    },

    "datu": {
        "display": "personas dati",
        "points": 3,
        "reason": "Tiek pieprasīti lietotāja personas dati."
    },

    "laimēj": {
        "display": "laimests",
        "points": 3,
        "reason": "Negaidīts paziņojums par laimestu var būt krāpniecības pazīme."
    },

    "balva": {
        "display": "balva",
        "points": 2,
        "reason": "Negaidīts paziņojums par balvu var būt krāpniecības pazīme."
    }
}

def analyze_email(subject, body):

    # Apvieno vēstules tematu un tekstu
    text = (subject + " " + body).lower()

    total_points = 0
    found_words = []

    # Meklē aizdomīgas pazīmes
    for word, information in suspicious_words.items():

        if word in text:

            total_points += information["points"]

            # Lietotājam parādām display nosaukumu,
            # nevis tehnisko vārda saīsinājumu
            found_words.append({
                "word": information["display"],
                "points": information["points"],
                "reason": information["reason"]
            })

    if total_points >= 7:

        result = "IESPĒJAMA PIKŠĶERĒŠANAS VĒSTULE"

    elif total_points >= 3:

        result = "AIZDOMĪGA VĒSTULE"

    else:

        result = "DROŠA VĒSTULE"

    return result, total_points, found_words

def analyze_csv(filename):

    try:

        # Nolasa CSV failu
        data = pd.read_csv(filename)

    except FileNotFoundError:

        print(f"\nKļūda: fails '{filename}' netika atrasts.")
        return

    except Exception as error:

        print(f"\nNeizdevās nolasīt failu: {error}")
        return

    print("\n")
    print("=" * 65)
    print("          PIKŠĶERĒŠANAS VĒSTUĻU DETEKTORS")
    print("=" * 65)

    for index, row in data.iterrows():

        subject = str(row.get("subject", ""))
        body = str(row.get("body", ""))

        result, points, found_words = analyze_email(
            subject,
            body
        )


        print("\n" + "-" * 65)

        print(f"VĒSTULE #{index + 1}")

        print(f"Temats: {subject}")

        print(f"\nRezultāts: {result}")

        print(f"Riska līmenis: {points} punkti")

        if found_words:

            print("\nAtrastās aizdomīgās pazīmes:")

            for item in found_words:

                print(f"\n  ⚠ {item['word']}")
                print(f"    +{item['points']} punkti")
                print(f"    Iemesls: {item['reason']}")

        else:

            print("\n  ✓ Aizdomīgas pazīmes netika atrastas.")

    print("\n" + "=" * 65)
    print("                 ANALĪZE PABEIGTA")
    print("=" * 65)

analyze_csv("emails.csv")

