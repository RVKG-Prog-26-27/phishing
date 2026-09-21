import csv
import random

subjects = [
    "Nepieciešama konta pārbaude",
    "Svarīgs drošības paziņojums",
    "Jūsu kontam nepieciešama pārbaude",
    "Neparasta aktivitāte kontā",
    "Konta piekļuves problēma",
    "Steidzams paziņojums",
    "Apstipriniet konta informāciju",
    "Drošības sistēmas brīdinājums",
    "Nepieciešama tūlītēja darbība",
    "Jūsu konts ir ierobežots",
    "Svarīga informācija par jūsu kontu",
    "Maksājuma apstiprināšana",
    "Darījuma pārbaude",
    "Identitātes pārbaude",
    "Konta darbības apstiprināšana",
    "Piekļuves atjaunošana",
    "Drošības pārbaude",
    "Paziņojums par konta darbību",
    "Nepieciešams apstiprinājums",
    "Brīdinājums par kontu",
    "Jūsu profils ir jāatjauno",
    "Konta pārbaudes termiņš",
    "Neapstiprināta darbība",
    "Svarīgs klienta paziņojums",
    "Pēdējais atgādinājums par kontu"
]

greetings = [
    "Labdien!",
    "Sveiki!",
    "Cienījamais klient!",
    "Labdien, cienījamais klient!",
    "Sveiki, klient!",
    "Cienījamais lietotāj!",
    "Labdien!",
    "Svarīgs paziņojums!"
]

problems = [
    "Mūsu sistēma ir konstatējusi neparastu aktivitāti jūsu kontā.",
    "Drošības sistēma ir pamanījusi aizdomīgu darbību.",
    "Pēdējās konta darbības dēļ nepieciešama papildu pārbaude.",
    "Automātiskā sistēma ir atzīmējusi jūsu kontu pārbaudei.",
    "Ir konstatēta darbība, kuru nepieciešams apstiprināt.",
    "Mūsu sistēmā ir reģistrēta neparasta piekļuves darbība.",
    "Kontam ir nepieciešama papildu drošības pārbaude.",
    "Sistēma nevarēja automātiski apstiprināt pēdējo darbību.",
    "Jūsu konta drošības statuss ir jāapstiprina.",
    "Ir konstatēta iespējama neatbilstība konta informācijā.",
    "Jūsu profils pašlaik gaida papildu pārbaudi.",
    "Automātiskās pārbaudes laikā tika konstatēta nepieciešamība atjaunināt informāciju."
]

actions = [
    "Lūdzu, apstipriniet savu konta informāciju.",
    "Lai turpinātu izmantot kontu, nepieciešams veikt pārbaudi.",
    "Lūdzu, pārbaudiet norādīto informāciju un apstipriniet darbību.",
    "Lai atjaunotu piekļuvi, nepieciešams apstiprināt konta statusu.",
    "Lūdzu, veiciet nepieciešamo pārbaudi pēc iespējas ātrāk.",
    "Lai izvairītos no piekļuves ierobežošanas, apstipriniet konta datus.",
    "Nepieciešams apstiprināt, ka konts joprojām pieder jums.",
    "Lūdzu, pabeidziet drošības pārbaudi.",
    "Lai turpinātu izmantot pakalpojumu, jāapstiprina jūsu informācija.",
    "Veiciet norādīto pārbaudi, lai atjaunotu pilnu piekļuvi."
]

urgency = [
    "Šo darbību nepieciešams veikt pēc iespējas ātrāk.",
    "Lūdzu, neatlieciet šo pārbaudi.",
    "Ja pārbaude netiks veikta, piekļuve kontam var tikt ierobežota.",
    "Pārbaudi ieteicams pabeigt tuvākajā laikā.",
    "Pretējā gadījumā dažas konta funkcijas var kļūt nepieejamas.",
    "Ja darbība netiks apstiprināta, konta izmantošana var būt ierobežota.",
    "Lūdzu, pievērsiet šim paziņojumam uzmanību.",
    "Pārbaudes termiņš ir ierobežots.",
    "Nepieciešams rīkoties pirms konta statusa maiņas.",
    "Pretējā gadījumā var tikt piemēroti papildu drošības ierobežojumi."
]

link_texts = [
    "Lai turpinātu, izmantojiet norādīto pārbaudes iespēju.",
    "Konta pārbaudi var pabeigt, izmantojot zemāk norādīto darbību.",
    "Lai apstiprinātu informāciju, atveriet pārbaudes sadaļu.",
    "Izmantojiet konta pārbaudes iespēju, lai turpinātu.",
    "Pabeidziet pārbaudi, izmantojot drošības sadaļu.",
    "Lai atjaunotu piekļuvi, turpiniet ar konta pārbaudi.",
    "Apstiprināšanas process ir pieejams konta pārbaudes sadaļā."
]

closings = [
    "Ar cieņu,\nKlientu apkalpošanas nodaļa.",
    "Ar cieņu,\nDrošības nodaļa.",
    "Paldies par sapratni.",
    "Paldies par sadarbību.",
    "Ar cieņu,\nAtbalsta komanda.",
    "Paldies, ka izmantojat mūsu pakalpojumus.",
    "Ar cieņu,\nKonta drošības komanda."
]

extra_sentences = [
    "Šis ir automātiski nosūtīts paziņojums.",
    "Atbildēt uz šo ziņojumu nav nepieciešams.",
    "Pārbaude tiek veikta drošības nolūkos.",
    "Paziņojums ir nosūtīts automātiski.",
    "Papildu informācija par pārbaudi ir pieejama konta sadaļā.",
    "Drošības pārbaude ir nepieciešama, lai aizsargātu jūsu kontu.",
    "Šī darbība ir saistīta ar jūsu konta drošību.",
    "Lūdzu, saglabājiet šo paziņojumu turpmākai atsaucei."
]


def create_email():
    subject = random.choice(subjects)
    greeting = random.choice(greetings)
    problem = random.choice(problems)
    action = random.choice(actions)

    # Izvēlamies nejaušu e-pasta struktūru
    style = random.randint(1, 5)

    if style == 1:
        message = (
            greeting + "\n\n" +
            problem + " " +
            action + " " +
            random.choice(urgency) + "\n\n" +
            random.choice(link_texts) + "\n\n" +
            random.choice(closings)
        )

    elif style == 2:
        message = (
            greeting + "\n\n" +
            "Vēlamies informēt par izmaiņām jūsu konta drošības statusā. " +
            problem + "\n\n" +
            action + " " +
            random.choice(link_texts) + "\n\n" +
            random.choice(urgency) + "\n\n" +
            random.choice(closings)
        )

    elif style == 3:
        message = (
            greeting + "\n\n" +
            problem + "\n\n" +
            random.choice(extra_sentences) + " " +
            action + "\n\n" +
            random.choice(urgency) + " " +
            random.choice(link_texts) + "\n\n" +
            random.choice(closings)
        )

    elif style == 4:
        message = (
            greeting + "\n\n" +
            "Svarīga informācija par jūsu kontu.\n\n" +
            problem + " " +
            random.choice(extra_sentences) + "\n\n" +
            action + "\n" +
            random.choice(link_texts) + "\n\n" +
            random.choice(urgency) + "\n\n" +
            random.choice(closings)
        )

    else:
        message = (
            greeting + "\n\n" +
            problem + "\n" +
            action + "\n\n" +
            random.choice(extra_sentences) + "\n\n" +
            random.choice(urgency) + " " +
            random.choice(link_texts) + "\n\n" +
            random.choice(closings)
        )

    return subject, message


with open(
    "phishing_emails.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.writer(file)

    writer.writerow(["subject", "message", "label"])

    for i in range(2000):
        subject, message = create_email()
        writer.writerow([subject, message, "phishing"])


print("Izveidoti 2000 dažādi sintētiski phishing e-pasti!")
print("Fails: phishing_emails.csv")