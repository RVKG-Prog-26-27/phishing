# Email Shield

## Projekta apraksts

**Email Shield** ir mašīnmācīšanās projekts e-pastu noteikšanai un klasificēšanai.

Sistēma klasificē e-pastus četrās kategorijās:

* **normal** — parasts e-pasts
* **advertising** — reklāmas e-pasts
* **spam** — mēstule
* **phishing** — pikšķerēšanas e-pasts

Projektu veido Flask serveris, mašīnmācīšanās modelis un Google Chrome paplašinājums, kas darbojas kopā ar Gmail.



## Nepieciešamā programmatūra

Lai palaistu projektu, nepieciešams:

* Python 3
* Google Chrome
* Gmail konts

Projektam nepieciešamas šādas Python bibliotēkas:

* pandas
* scikit-learn
* joblib
* Flask
* flask-cors

---

## Instalēšana

Atveriet **PowerShell**  un pārejiet uz projekta `detector` mapi.

Piemērs:

```powershell
cd path\to\email_shield\detector
```

Instalējiet nepieciešamās bibliotēkas:

```powershell
py -m pip install pandas scikit-learn joblib flask flask-cors
```

---

## Projekta palaišana

### 1. Flask servera palaišana

PowerShell logā, atrodoties `detector` mapē, palaidiet:

```powershell
py app.py
```

Ja serveris ir palaists veiksmīgi, terminālī būs redzams:

```text
Email Shield

Serveris darbojas:
http://127.0.0.1:5000
```

**Svarīgi:** neatveriet šo termināli ciet, kamēr izmantojat projektu.

Flask serveris izmanto šādus jau apmācītus failus:

```text
email_model_real.pkl
tfidf_vectorizer_real.pkl
```

---

### 2. Tīmekļa saskarnes atvēršana

## Google Chrome paplašinājums

Projektā ir iekļauts Google Chrome paplašinājums, kas darbojas Gmail vidē.

### Paplašinājuma pievienošana

1. Atveriet Google Chrome.
2. Adreses joslā ievadiet:

```text
chrome://extensions/
```

3. Ieslēdziet **Developer mode** jeb **Izstrādātāja režīmu**.
4. Nospiediet **Load unpacked**.
5. Izvēlieties projekta mapi:

```text
email_shield/chrome_extension
```

6. Pārliecinieties, ka paplašinājums ir ieslēgts.
7. Atveriet Gmail:

```text
https://mail.google.com/
```

8. Atsvaidziniet Gmail lapu.

Paplašinājums analizē Gmail e-pastus un parāda to kategoriju blakus e-pastam.

---

## Kā darbojas sistēma

```text
Gmail
   ↓
Google Chrome paplašinājums
   ↓
Flask API
   ↓
TF-IDF vektorizators
   ↓
Logistic Regression modelis
   ↓
E-pasta kategorija
   ↓
Google Chrome paplašinājums
   ↓
Kategorija tiek parādīta Gmail
```

Chrome paplašinājums pats neveic mašīnmācīšanās klasifikāciju.

Tas:

1. Atrod e-pastus Gmail.
2. Iegūst e-pasta tekstu.
3. Nosūta tekstu Flask serverim.
4. Saņem prognozēto kategoriju.
5. Parāda kategoriju Gmail saskarnē.

Flask serveris izmanto apmācīto mašīnmācīšanās modeli e-pasta klasificēšanai.

---

## Mašīnmācīšanās modelis

Modeļa apmācībai tiek izmantots fails:

```text
real_latvian_emails_fixed.csv
```

Datu kopā ir šādas kolonnas:

```text
sender
subject
message
label
```

Modeļa izveidē tiek izmantotas:

* **TF-IDF**
* **Logistic Regression**

Modeļa apmācības fails:

```text
detector/train_model.py
```

### Modeļa atkārtota apmācība

Parasti modeļa atkārtota apmācība nav nepieciešama, lai palaistu projektu.

Ja tiek mainīta datu kopa un modeli nepieciešams apmācīt no jauna, PowerShell logā, atrodoties `detector` mapē, palaidiet:

```powershell
py train_model.py
```

Rezultātā tiks izveidoti vai atjaunināti:

```text
email_model_real.pkl
tfidf_vectorizer_real.pkl
```

Pēc modeļa atkārtotas apmācības Flask serveris jāpalaiž no jauna:

```powershell
py app.py
```

---

## API

Flask serveris nodrošina `/analyze` API.

### POST `/analyze`

Chrome paplašinājums nosūta e-pasta tekstu uz:

```text
http://127.0.0.1:5000/analyze
```

Serveris atgriež:

* prognozēto e-pasta kategoriju;
* katras kategorijas varbūtību;
* pikšķerēšanas varbūtību;
* parasta e-pasta varbūtību;
* mēstules varbūtību;
* reklāmas e-pasta varbūtību;
* identificētos draudu indikatorus.

---

## E-pasta kategorijas

| Kategorija    | Nozīme                |
| ------------- | --------------------- |
| `normal`      | Parasts e-pasts       |
| `advertising` | Reklāmas e-pasts      |
| `spam`        | Mēstule               |
| `phishing`    | Pikšķerēšanas e-pasts |

---

## Problēmu novēršana

### Flask serveris nepalaižas

Pārliecinieties, ka atrodaties `detector` mapē:

```powershell
cd path\to\email_shield\detector
```

Pēc tam palaidiet:

```powershell
py app.py
```

Ja nepieciešams, atkārtoti instalējiet bibliotēkas:

```powershell
py -m pip install pandas scikit-learn joblib flask flask-cors
```

### Chrome paplašinājums nedarbojas

Pārbaudiet, vai:

* Flask serveris darbojas adresē `http://127.0.0.1:5000`;
* Chrome paplašinājums ir ieslēgts;
* `chrome_extension` mape tika pievienota ar **Load unpacked**;
* Gmail lapa tika atsvaidzināta pēc paplašinājuma pievienošanas vai pārlādēšanas.

### Trūkst modeļa failu

`detector` mapē jāatrodas šādiem failiem:

```text
email_model_real.pkl
tfidf_vectorizer_real.pkl
```

Ja šo failu nav, modeli nepieciešams izveidot no jauna, palaižot:

```powershell
py train_model.py
```
## Testēšanas rezultāti

### 1. Klasifikācijas rezultātu matrica

| Īstā kategorija ↓ / Prognozētā kategorija → | Normal | Advertising | Spam | Phishing | Pareizi noteikts |
|---|---:|---:|---:|---:|---:|
| Normal | 10 | 0 | 0 | 0 | 10 |
| Advertising | 0 | 1 | 0 | 0 | 1 |
| Spam | 1 | 1 | 6 | 0 | 6 |
| Phishing | 0 | 0 | 0 | 1 | 1 |

### 2. Klasifikācijas kvalitātes rādītāji

- **Precision** = pareizi noteiktās kategorijas vēstules / visas modelim piešķirtās šīs kategorijas vēstules.
- **Recall** = pareizi noteiktās kategorijas vēstules / visas reālās šīs kategorijas vēstules.
- **Accuracy** = visu pareizi klasificēto vēstuļu skaits / kopējais vēstuļu skaits.

| Kategorija | Precision | Recall | Accuracy |
|---|---:|---:|---:|
| Normal | 90% | 100% | 95% |
| Advertising | 50% | 100% | 95% |
| Spam | 100% | 75% | 90% |
| Phishing | 100% | 100% | 100% |

### 3. Kopējais rezultāts

**Overall Accuracy = 18/20 × 100 = 90%**

Testēšanas laikā tika pārbaudīti 20 e-pasti četrās kategorijās. Modelis pareizi klasificēja 18 e-pastus, sasniedzot 90% kopējo Accuracy.

Galvenie secinājumi:

Normal un Phishing kategoriju Recall sasniedza 100%.
Advertising kategorijas Precision bija 50%, tāpēc nepieciešams uzlabot reklāmu atšķiršanu no citām kategorijām.
Spam kategorijas Recall bija 75%, kas norāda uz dažām klasifikācijas kļūdām.

Secinājums: Modelis spēj klasificēt e-pastus četrās kategorijās, sasniedzot 90% kopējo Accuracy. Turpmāk nepieciešams uzlabot Advertising un Spam kategoriju atpazīšanu.
