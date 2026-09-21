import pandas as pd
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

random.seed(42)


# ============================================================
# PHISHING PIEMĒRI
# ============================================================

phishing_templates = [

    # -------------------------
    # DARBA KRĀPNIECĪBA
    # -------------------------

    {
        "subjects": [
            "Darba piedāvājums",
            "Darbs no mājām",
            "Iespēja nopelnīt papildus",
            "Steidzams darba piedāvājums",
            "Attālināta darba iespēja"
        ],
        "messages": [
            "Vēlies nopelnīt vairāk naudas un strādāt mazāk? Nav nepieciešama iepriekšēja pieredze. Lai sāktu, sazinieties ar mums Telegram.",
            "Piedāvājam darbu no mājām ar ļoti augstu atalgojumu. Darbs aizņem tikai dažas stundas dienā. Lai pieteiktos, izmantojiet norādīto saiti.",
            "Meklējam cilvēkus vienkāršam darbam internetā. Iespējams nopelnīt lielu summu katru dienu. Uzrakstiet mūsu pārstāvim Telegram.",
            "Jums ir iespēja iegūt labi apmaksātu darbu bez pieredzes. Vietu skaits ir ierobežots. Reģistrējieties, izmantojot norādīto saiti."
        ]
    },

    # -------------------------
    # TELEGRAM / WHATSAPP
    # -------------------------

    {
        "subjects": [
            "Svarīgs paziņojums",
            "Jums ir jauna ziņa",
            "Saziņa ar mūsu speciālistu",
            "Darba iespēja Telegram",
            "Apstipriniet saziņu"
        ],
        "messages": [
            "Lai saņemtu papildu informāciju, pievienojieties mūsu Telegram kanālam.",
            "Mūsu konsultants gaida jūsu ziņu Telegram. Uzrakstiet vārdu Gatavs, lai turpinātu.",
            "Lai pabeigtu reģistrāciju, sazinieties ar mūsu speciālistu Telegram.",
            "Informācija par piedāvājumu pieejama WhatsApp. Noklikšķiniet uz saites un sazinieties ar konsultantu."
        ]
    },

    # -------------------------
    # PIEGĀDES
    # -------------------------

    {
        "subjects": [
            "Jūsu sūtījuma piegāde",
            "Nepieciešama informācija par sūtījumu",
            "Sūtījuma piegāde apturēta",
            "Piegādes problēma",
            "Svarīgi par jūsu paciņu"
        ],
        "messages": [
            "Jūsu sūtījumu nevar piegādāt, jo nepieciešams apstiprināt piegādes adresi. Izmantojiet norādīto saiti.",
            "Jūsu paciņa ir aizturēta. Lai turpinātu piegādi, nepieciešams apstiprināt informāciju.",
            "Nepieciešams veikt nelielu maksājumu, lai pabeigtu sūtījuma piegādi.",
            "Jūsu sūtījuma piegāde ir apturēta. Lai atjaunotu piegādi, nekavējoties apstipriniet savus datus."
        ]
    },

    # -------------------------
    # BANKA / MAKSĀJUMI
    # -------------------------

    {
        "subjects": [
            "Nepieciešama konta pārbaude",
            "Svarīgs paziņojums par jūsu kontu",
            "Konta drošības pārbaude",
            "Maksājuma apstiprināšana",
            "Jūsu kontam nepieciešama uzmanība"
        ],
        "messages": [
            "Mūsu drošības sistēma ir konstatējusi neparastu aktivitāti jūsu kontā. Nekavējoties apstipriniet savus datus.",
            "Lai novērstu konta bloķēšanu, nepieciešams atkārtoti apstiprināt jūsu personas un maksājumu informāciju.",
            "Jūsu pēdējais maksājums nav apstiprināts. Izmantojiet norādīto saiti, lai pārbaudītu maksājuma informāciju.",
            "Ja pārbaude netiks veikta tuvāko 24 stundu laikā, piekļuve kontam var tikt ierobežota."
        ]
    },

    # -------------------------
    # PAROLES
    # -------------------------

    {
        "subjects": [
            "Paroles derīguma termiņš",
            "Atjauniniet savu paroli",
            "Konta drošības brīdinājums",
            "Nepieciešama paroles maiņa"
        ],
        "messages": [
            "Jūsu parole drīzumā zaudēs derīgumu. Lai saglabātu piekļuvi kontam, ievadiet pašreizējo paroli un izveidojiet jaunu.",
            "Drošības apsvērumu dēļ nepieciešams apstiprināt paroli.",
            "Jūsu kontā konstatēta aizdomīga aktivitāte. Lai aizsargātu kontu, veiciet paroles pārbaudi."
        ]
    },

    # -------------------------
    # BALVAS
    # -------------------------

    {
        "subjects": [
            "Apsveicam! Jūs esat laimējis",
            "Jūsu balva ir gatava",
            "Aicinām saņemt balvu",
            "Jūs esat izvēlēts"
        ],
        "messages": [
            "Apsveicam! Jūs esat izvēlēts īpašai balvai. Lai saņemtu balvu, apstipriniet savus datus.",
            "Jūsu balva ir rezervēta. Lai to saņemtu, aizpildiet reģistrācijas formu.",
            "Jums ir piešķirta naudas balva. Lai pārskaitītu naudu, nepieciešams ievadīt bankas informāciju."
        ]
    },

    # -------------------------
    # SOCIĀLIE TĪKLI
    # -------------------------

    {
        "subjects": [
            "Jūsu konts tiks bloķēts",
            "Svarīgs paziņojums par jūsu profilu",
            "Konta drošības brīdinājums",
            "Nepieciešama profila pārbaude"
        ],
        "messages": [
            "Esam konstatējuši aizdomīgu darbību jūsu profilā. Lai izvairītos no konta bloķēšanas, apstipriniet savu identitāti.",
            "Jūsu profils ir saņēmis drošības brīdinājumu. Nekavējoties veiciet pārbaudi, izmantojot norādīto saiti.",
            "Ja identitāte netiks apstiprināta, jūsu konts var tikt deaktivizēts."
        ]
    },

    # -------------------------
    # PERSONAS DATI
    # -------------------------

    {
        "subjects": [
            "Nepieciešama identitātes pārbaude",
            "Apstipriniet savus personas datus",
            "Svarīga drošības pārbaude",
            "Datu atjaunošana"
        ],
        "messages": [
            "Lai turpinātu izmantot pakalpojumu, nepieciešams apstiprināt vārdu, personas kodu un kontaktinformāciju.",
            "Jūsu personas dati ir jāatjauno. Izmantojiet norādīto saiti, lai aizpildītu pārbaudes formu.",
            "Drošības pārbaudes laikā nepieciešams ievadīt pieprasīto personisko informāciju."
        ]
    },

    # -------------------------
    # KRIPTOVALŪTA
    # -------------------------

    {
        "subjects": [
            "Īpaša investīciju iespēja",
            "Palieliniet savus ienākumus",
            "Kriptovalūtas investīciju piedāvājums",
            "Ekskluzīva peļņas iespēja"
        ],
        "messages": [
            "Izmantojiet mūsu sistēmu un nopelniet līdz pat 500 eiro dienā. Lai sāktu, veiciet sākotnējo iemaksu.",
            "Mūsu eksperti palīdzēs jums ātri palielināt ienākumus ar kriptovalūtu. Reģistrējieties, izmantojot saiti.",
            "Ekskluzīva investīciju iespēja ar garantētu peļņu. Vietu skaits ir ierobežots."
        ]
    },

    # -------------------------
    # STEIDZAMĪBA
    # -------------------------

    {
        "subjects": [
            "NEKAVĒJOTIES RĪKOJIETIES",
            "Steidzams paziņojums",
            "Svarīgi! Nepieciešama tūlītēja rīcība",
            "Pēdējais brīdinājums"
        ],
        "messages": [
            "Šī ir pēdējā iespēja apstiprināt jūsu kontu. Rīkojieties nekavējoties.",
            "Ja nepieciešamā darbība netiks veikta 24 stundu laikā, jūsu konts tiks bloķēts.",
            "Lūdzu, nekavējoties veiciet pārbaudi, lai nezaudētu piekļuvi pakalpojumam."
        ]
    }
]


# ============================================================
# SAITES
# ============================================================

links = [
    "https://t.me/darbs_online",
    "https://t.me/fast_work",
    "https://t.me/earn_money_lv",
    "https://example-login-check.com",
    "https://account-security-check.com",
    "https://delivery-confirmation.example",
    "https://payment-verification.example"
]


# ============================================================
# ĢENERĒJAM PHISHING PIEMĒRUS
# ============================================================

phishing_emails = []

for template in phishing_templates:

    for _ in range(80):

        subject = random.choice(template["subjects"])
        message = random.choice(template["messages"])

        # Daļai vēstuļu pievienojam saiti
        if random.random() < 0.75:
            message += (
                "\n\nLai turpinātu, izmantojiet norādīto saiti:\n"
                + random.choice(links)
            )

        # Daļai pievienojam steidzamību
        if random.random() < 0.4:
            message += (
                "\n\nLūdzu, rīkojieties pēc iespējas ātrāk."
            )

        phishing_emails.append({
            "subject": subject,
            "message": message,
            "label": "phishing"
        })


# ============================================================
# NORMAL E-PASTI
# ============================================================

normal_templates = [

    {
        "subjects": [
            "Darba sanāksme",
            "Darba uzdevums",
            "Nedēļas darba plāns",
            "Informācija par projektu"
        ],
        "messages": [
            "Sveiki! Nosūtu informāciju par nākamās nedēļas darba plānu. Sanāksme notiks pirmdien plkst. 10.00.",
            "Labdien! Pielikumā nosūtu dokumentu ar projekta uzdevumiem. Ja rodas jautājumi, varam tos pārrunāt sanāksmē.",
            "Sveiki, kolēģi! Atgādinu par rītdienas tikšanos. Lūdzu, sagatavojiet informāciju par paveiktajiem uzdevumiem."
        ]
    },

    {
        "subjects": [
            "Pasūtījuma informācija",
            "Jūsu pasūtījums",
            "Piegādes informācija",
            "Pasūtījuma statuss"
        ],
        "messages": [
            "Labdien! Informējam, ka jūsu pasūtījums ir saņemts un tiks sagatavots nosūtīšanai.",
            "Sveiki! Jūsu pasūtījums ir nodots kurjeram. Piegāde paredzēta tuvāko darba dienu laikā.",
            "Informējam, ka pasūtījuma sagatavošana ir pabeigta. Piegādes informācija pieejama jūsu klienta kontā."
        ]
    },

    {
        "subjects": [
            "Tikšanās apstiprinājums",
            "Tikšanās laika maiņa",
            "Sanāksmes informācija",
            "Tikšanās rīt"
        ],
        "messages": [
            "Labdien! Vēlos apstiprināt mūsu tikšanos rīt plkst. 14.00.",
            "Sveiki! Vai mums būtu iespējams pārcelt tikšanos uz ceturtdienu plkst. 15.00?",
            "Labdien! Atgādinu, ka mūsu tikšanās notiks rīt plkst. 10.30."
        ]
    },

    {
        "subjects": [
            "Aptauja par pakalpojumu",
            "Jūsu atsauksme",
            "Aptaujas anketa",
            "Klientu aptauja"
        ],
        "messages": [
            "Labdien! Vēlamies uzzināt jūsu viedokli par mūsu pakalpojumu. Aptaujas aizpildīšana aizņems aptuveni piecas minūtes.",
            "Sveiki! Būsim pateicīgi, ja dalīsieties ar savu pieredzi un sniegsiet atsauksmi par mūsu pakalpojumu.",
            "Labdien! Nosūtām jums īsu klientu aptauju par nesen saņemto pakalpojumu."
        ]
    },

    {
        "subjects": [
            "Mācību materiāli",
            "Nodarbības informācija",
            "Mājasdarbs",
            "Kursa materiāli"
        ],
        "messages": [
            "Sveiki! Pielikumā nosūtu šīs nedēļas mācību materiālus.",
            "Labdien! Atgādinu, ka nākamajā nodarbībā apskatīsim iepriekš nosūtīto materiālu.",
            "Sveiki! Nosūtu mājasdarba uzdevumu un tā izpildes termiņu."
        ]
    }
]


normal_emails = []

for template in normal_templates:

    for _ in range(100):

        subject = random.choice(template["subjects"])
        message = random.choice(template["messages"])

        normal_emails.append({
            "subject": subject,
            "message": message,
            "label": "normal"
        })


# ============================================================
# SAGLABĀŠANA
# ============================================================

phishing_df = pd.DataFrame(phishing_emails)
normal_df = pd.DataFrame(normal_emails)


# Ielādējam sākotnējos datus
old_phishing = pd.read_csv(
    BASE_DIR / "latvian_phishing_2000.csv"
)

old_normal = pd.read_csv(
    BASE_DIR / "latvian_normal_2000.csv"
)


# Apvienojam
all_phishing = pd.concat(
    [old_phishing, phishing_df],
    ignore_index=True
)

all_normal = pd.concat(
    [old_normal, normal_df],
    ignore_index=True
)


# Noņemam dublikātus
all_phishing = all_phishing.drop_duplicates(
    subset=["subject", "message"]
)

all_normal = all_normal.drop_duplicates(
    subset=["subject", "message"]
)


# Saglabājam
all_phishing.to_csv(
    BASE_DIR / "latvian_phishing_extended.csv",
    index=False,
    encoding="utf-8-sig"
)

all_normal.to_csv(
    BASE_DIR / "latvian_normal_extended.csv",
    index=False,
    encoding="utf-8-sig"
)


print("=" * 60)
print("DATU KOPUMS IR UZLABOTS")
print("=" * 60)

print(f"\nPhishing vēstules: {len(all_phishing)}")
print(f"Normal vēstules: {len(all_normal)}")

print("\nJaunie piemēri:")
print(f"Phishing: {len(phishing_df)}")
print(f"Normal: {len(normal_df)}")

print("\nIzveidoti faili:")
print("latvian_phishing_extended.csv")
print("latvian_normal_extended.csv")

print("\nDatu kopuma uzlabošana pabeigta!")