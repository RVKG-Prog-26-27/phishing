# Email Shield

## 1. Projekta apraksts

**Email Shield** ir e-pasta drošības projekts, kas izmanto mašīnmācīšanos, lai klasificētu e-pasta ziņojumus un palīdzētu lietotājiem atpazīt potenciāli aizdomīgus ziņojumus.

Sistēma klasificē e-pastus četrās kategorijās:

- `normal` — parasti e-pasta ziņojumi.
- `advertising` — reklāmas un komerciāli piedāvājumi.
- `spam` — nevēlami e-pasta ziņojumi.
- `phishing` — ziņojumi, kas var mēģināt iegūt personas datus vai piekļuvi lietotāja kontiem.

Projektā ir iekļauts mašīnmācīšanās modelis, Flask servera puse un Chrome pārlūkprogrammas paplašinājums.

## 2. Projekta mērķis

Projekta mērķis ir izveidot sistēmu, kas analizē e-pasta ziņojumu tekstu, nosaka tā kategoriju un sniedz lietotājam informāciju par klasifikācijas rezultātu.

Sistēma ir paredzēta, lai demonstrētu mašīnmācīšanās izmantošanu e-pasta klasifikācijā un potenciāli aizdomīgu ziņojumu atpazīšanā.

## 3. Izmantotās tehnoloģijas

Projektā tiek izmantotas šādas tehnoloģijas:

- **Python** — modeļa apmācībai un servera puses izstrādei.
- **Flask** — tīmekļa servera un API izveidei.
- **Flask-CORS** — starpdomēnu pieprasījumu atbalstam.
- **scikit-learn** — teksta apstrādei un mašīnmācīšanās modeļa izveidei.
- **TF-IDF Vectorizer** — teksta pārveidošanai skaitliskās pazīmēs.
- **Logistic Regression** — e-pasta ziņojumu klasificēšanai.
- **Joblib** — apmācītā modeļa un vektorizatora saglabāšanai un ielādei.
- **HTML, CSS un JavaScript** — lietotāja saskarnes un Chrome paplašinājuma izstrādei.
- **Chrome Extensions API** — pārlūkprogrammas paplašinājuma funkcionalitātei.

## 4. Sistēmas arhitektūra

Projektu veido trīs galvenās daļas.

### 4.1. Mašīnmācīšanās modelis

Mašīnmācīšanās modelis tiek apmācīts, izmantojot marķētu e-pastu datu kopu. Katram e-pastam ir piešķirta viena no četrām kategorijām.

Teksts tiek pārveidots skaitliskās pazīmēs, izmantojot TF-IDF, un pēc tam tiek izmantots Logistic Regression klasifikatora apmācībai.

Apmācītais modelis un vektorizators tiek saglabāti failos:

- `email_model_real.pkl`
- `tfidf_vectorizer_real.pkl`

Šos failus ielādē servera puse, lai klasificētu jaunus e-pasta ziņojumus.

### 4.2. Flask servera puse

Servera puse ir izveidota Python vidē, izmantojot Flask.

Tā saņem e-pasta tematu un ziņojuma tekstu, nodod tos mašīnmācīšanās modelim un atgriež klasifikācijas rezultātu.

Servera puses galvenais fails ir `app.py`.

### 4.3. Chrome paplašinājums

Chrome paplašinājums ir paredzēts darbam ar Gmail un nodrošina lietotāja saskarni e-pastu analīzei.

Paplašinājuma komponenti ietver uznirstošo logu, fona servisa skriptu un satura skriptu. Tie nodrošina paplašinājuma saskarni un mijiedarbību ar pārlūkprogrammu un servera pusi.

## 5. E-pastu datu kopa

E-pastu datu kopa tiek glabāta CSV formātā. Tā satur četras kolonnas:

| Kolonna | Apraksts |
|---|---|
| `sender` | E-pasta sūtītāja adrese |
| `subject` | E-pasta temats |
| `message` | E-pasta ziņojuma teksts |
| `label` | E-pasta kategorija |

Kolonna `label` norāda, kurai kategorijai attiecīgais e-pasts pieder.

Saskaņā ar iepriekš iegūtajiem apmācības rezultātiem datu kopā ir 166 e-pasti:

| Kategorija | E-pastu skaits |
|---|---:|
| `normal` | 85 |
| `advertising` | 44 |
| `phishing` | 21 |
| `spam` | 16 |
| **Kopā** | **166** |

Datu kopas kvalitāte un piemēru skaits katrā kategorijā var ietekmēt modeļa klasifikācijas rezultātus.

## 6. Mašīnmācīšanās modeļa apmācība

Modeļa apmācības skripts ielādē datu kopu, sagatavo tekstu, pārveido to ar TF-IDF un apmāca Logistic Regression klasifikatoru.

Apmācības process ietver šādus soļus:

1. E-pastu datu kopas ielāde.
2. E-pastu teksta un kategoriju marķējumu sagatavošana.
3. Teksta pārveidošana skaitliskās TF-IDF pazīmēs.
4. Logistic Regression klasifikatora apmācība.
5. Apmācītā modeļa un vektorizatora saglabāšana ar Joblib.

Pēc apmācības izveidotie `.pkl` faili tiek izmantoti servera pusē.

**Svarīgi:** modeļa apmācībā izmantotajiem teksta laukiem jāsakrīt ar laukiem, kurus izmanto klasifikācijas laikā. Pašreizējā `app.py` kodā modelim tiek nodots e-pasta temats un ziņojuma teksts, bet sūtītāja adrese netiek izmantota.

## 7. Servera puses darbība

Servera puses galvenais fails ir `app.py`.

### 7.1. Modeļa ielāde

Lietotne izmanto `pathlib`, lai noteiktu modeļa un vektorizatora failu atrašanās vietu attiecībā pret `app.py` failu.

Modeļa faili tiek ielādēti, izmantojot Joblib, uzsākot servera darbību.

### 7.2. E-pasta klasificēšana

Funkcija `classify_email(subject, message)` veic šādas darbības:

1. Apvieno e-pasta tematu un ziņojuma tekstu.
2. Pārveido tekstu, izmantojot apmācīto TF-IDF vektorizatoru.
3. Nosaka prognozēto e-pasta kategoriju.
4. Iegūst modeļa prognozētās varbūtības katrai kategorijai.
5. Izveido paskaidrojumus, izmantojot iepriekš definētus atslēgvārdus.
6. Atgriež rezultātu vārdnīcas formā.

### 7.3. Rezultāta paskaidrojumi

Funkcija `explain_email()` analizē e-pasta tematu un tekstu, pārveidojot tos mazajos burtos, un meklē iepriekš definētus atslēgvārdus.

Atkarībā no prognozētās kategorijas tiek meklētas šādas pazīmes:

- Steidzamības izteicieni.
- Paroļu un identitātes pārbaudes pieprasījumi.
- Aizdomīgas konta darbības vai konta ierobežošanas draudi.
- Aicinājumi atvērt saites.
- Paziņojumi par laimestiem un balvām.
- Reklāmas, atlaides un komerciāli piedāvājumi.

Funkcija atgriež paskaidrojumus, pamatojoties uz atrastajām pazīmēm.

Šie paskaidrojumi tiek veidoti ar iepriekš definētu noteikumu palīdzību. Tie nav mašīnmācīšanās modeļa patstāvīgi ģenerēts skaidrojums un negarantē, ka e-pasts ir drošs vai bīstams.

## 8. API galapunkti

### 8.1. E-pasta analīze

**Metode:** `POST`

**Adrese:** `/analyze`

Galapunkts pieņem JSON pieprasījumu ar e-pasta tematu un ziņojuma tekstu.

Pieprasījuma piemērs:

```json
{
  "subject": "Verify your account",
  "message": "Please verify your account information."
}
```

Atbildes struktūras piemērs:

```json
{
  "prediction": "phishing",
  "category": "phishing",
  "reasons": [
    "Example explanation based on configured keyword rules"
  ],
  "probabilities": {
    "advertising": 5.25,
    "normal": 10.5,
    "phishing": 80.25,
    "spam": 4.0
  },
  "phishing_probability": 80.25,
  "normal_probability": 10.5,
  "spam_probability": 4.0,
  "advertising_probability": 5.25
}
```

Norādītās vērtības ir tikai piemērs, kas parāda atbildes struktūru, nevis reāla e-pasta analīzes rezultāts.

Atbilde satur prognozēto kategoriju, paskaidrojumus un visu četru kategoriju varbūtību novērtējumus procentos. Vērtības tiek noapaļotas līdz divām zīmēm aiz komata.

### 8.2. Tīmekļa saskarne

**Adrese:** `/`

- `GET` pieprasījums parāda tīmekļa saskarni, izmantojot veidni `templates/index.html`.
- `POST` pieprasījums saņem tematu un ziņojuma tekstu no formas, klasificē e-pastu un parāda rezultātu.

## 9. Servera palaišana

### Prasības

Lai palaistu servera pusi, nepieciešams:

- Instalēts Python.
- Pieejami projekta faili.
- Modeļa un vektorizatora faili norādītajā atrašanās vietā.

### Nepieciešamo bibliotēku instalēšana

Terminālī izpildi:

```bash
pip install flask flask-cors joblib scikit-learn
```

Ja projektā tiek izmantotas papildu bibliotēkas, tās jāinstalē atbilstoši projekta atkarībām.

### Servera palaišana

Terminālī atver direktoriju, kurā atrodas `app.py`, un izpildi:

```bash
python app.py
```

Ja serveris tiek palaists veiksmīgi, tas darbojas adresē:

`http://127.0.0.1:5000`

Palaišanas laikā terminālī tiek parādīts projekta nosaukums un modeļa atbalstītās kategorijas.

Lai Chrome paplašinājums varētu nosūtīt pieprasījumus lokālajam API, serverim jābūt ieslēgtam.

Pašreizējā kodā ir ieslēgts Flask atkļūdošanas režīms (`debug=True`). Tas paredzēts lokālai izstrādei, nevis produkcijas videi.

## 10. Chrome paplašinājuma integrācija

Chrome paplašinājums ir paredzēts, lai savienotu Gmail saskarni ar Flask servera pusi.

Vispārējā darbplūsma:

1. Lietotājs atver vai izvēlas e-pastu Gmail vidē.
2. Paplašinājums iegūst analīzei nepieciešamo e-pasta informāciju.
3. Paplašinājums nosūta pieprasījumu servera pusei.
4. Servera puse klasificē e-pastu.
5. Paplašinājums parāda saņemto kategoriju un saistīto informāciju.

Precīza darbība ir atkarīga no pašreizējās paplašinājuma JavaScript un HTML implementācijas.

Pašreizējā servera pusē klasifikācijai tiek izmantots e-pasta temats un ziņojuma teksts. Lai gan datu kopā ir arī sūtītāja lauks, pašreizējais `app.py` kods to neizmanto modeļa ievadē.

## 11. Testēšana

Projektu ieteicams testēt ar piemēriem no visām četrām kategorijām:

- Parasti personiski vai informatīvi e-pasti.
- Reklāmas un komerciāli piedāvājumi.
- Nevēlami masveida ziņojumi.
- Ziņojumi ar iespējamām pikšķerēšanas pazīmēm.

Testēšanas laikā jāpārbauda:

- Vai prognozētā kategorija atbilst e-pasta saturam.
- Vai API atgriež paredzēto JSON struktūru.
- Vai tiek atgrieztas visu kategoriju varbūtības.
- Vai paskaidrojumu funkcija atrod definētos atslēgvārdus.
- Vai Chrome paplašinājums veiksmīgi sazinās ar servera pusi.
- Vai lietotāja saskarne pareizi parāda klasifikācijas rezultātu.

Modeļa veiktspējas novērtēšanai ieteicams izmantot atsevišķu testēšanas datu kopu. Var izmantot tādus rādītājus kā precizitāte (*accuracy*), precision, recall, F1-score un kļūdu matricu (*confusion matrix*).

## 12. Ierobežojumi

Pašreizējai sistēmai ir vairāki ierobežojumi:

- Apmācības datu kopa ir neliela, un kategoriju piemēru skaits atšķiras.
- Klasifikācijas kvalitāte ir atkarīga no datu kopas kvalitātes un daudzveidības.
- Modelis analizē tematu un ziņojuma tekstu, bet neizmanto sūtītāja adresi.
- Paskaidrojumu sistēma balstās uz iepriekš definētiem atslēgvārdiem un var neatpazīt visas aizdomīga satura pazīmes.
- Modeļa varbūtību novērtējumi negarantē, ka ziņojums pieder konkrētai kategorijai.
- Servera puse neatkarīgi nepārbauda URL adreses, sūtītāja autentiskumu, pielikumus vai e-pasta galvenes.
- Pašreizējā lokālā servera konfigurācija ir paredzēta izstrādei, nevis produkcijas videi.

Tāpēc klasifikācijas rezultāts jāuztver kā iespējamā riska indikators, nevis galīgs drošības spriedums.

## 13. Iespējamie uzlabojumi

Nākotnē projektu var uzlabot, veicot šādus uzdevumus:

- Paplašināt datu kopu ar vairāk piemēriem katrā kategorijā.
- Novērtēt modeļa veiktspēju, izmantojot atsevišķu testēšanas datu kopu.
- Nodrošināt, ka apmācībā un klasifikācijā tiek izmantoti vienādi teksta lauki.
- Uzlabot daudzvalodu e-pastu atpazīšanu.
- Pievienot ievades datu pārbaudi, tostarp tukšu lauku apstrādi.
- Uzlabot paskaidrojumu sistēmu un samazināt kļūdainas klasifikācijas gadījumus.
- Papildināt sistēmu ar URL analīzi un citām pikšķerēšanas pazīmēm.
- Uzlabot kļūdu apstrādi un lietotāja saskarni.
- Sagatavot atkarību sarakstu, lai atvieglotu projekta instalēšanu un palaišanu.

## 14. Secinājumi

**Email Shield** apvieno mašīnmācīšanos, Flask servera pusi un Chrome pārlūkprogrammas paplašinājumu, lai klasificētu e-pasta ziņojumus četrās kategorijās: parasti ziņojumi, reklāmas, mēstules un pikšķerēšanas ziņojumi.

Projekts demonstrē teksta klasifikācijas integrēšanu pārlūkprogrammas vidē, lai palīdzētu lietotājiem atpazīt potenciāli aizdomīgus e-pasta ziņojumus.

Sistēmas uzticamība ir atkarīga no apmācības datu kvalitātes, vienotas ievades apstrādes un turpmākas testēšanas un pilnveidošanas.
