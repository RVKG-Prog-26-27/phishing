console.log("Latvian Email Security: scanner started");

const API_URL = "http://127.0.0.1:5000/analyze";


// ==========================================
// Создание пузырька
// ==========================================

function createBubble(probability) {

    if (probability < 25) {
        return null;
    }

    const bubble = document.createElement("span");

    bubble.className = "latvian-phishing-bubble";

    bubble.textContent =
        `${Math.round(probability)}%`;

    bubble.style.display = "inline-flex";
    bubble.style.alignItems = "center";
    bubble.style.justifyContent = "center";

    bubble.style.minWidth = "44px";
    bubble.style.height = "26px";

    bubble.style.padding = "0 8px";
    bubble.style.marginLeft = "8px";

    bubble.style.borderRadius = "14px";

    bubble.style.color = "white";
    bubble.style.fontSize = "12px";
    bubble.style.fontWeight = "bold";
    bubble.style.fontFamily = "Arial, sans-serif";

    bubble.style.verticalAlign = "middle";

    if (probability <= 50) {

        // 25–50% — oranžs
        bubble.style.backgroundColor = "#f59e0b";

    } else {

        // >50% — sarkans
        bubble.style.backgroundColor = "#dc2626";
    }

    bubble.title =
        `Phishing varbūtība: ${probability.toFixed(2)}%`;

    return bubble;
}


// ==========================================
// Анализ письма из списка
// ==========================================

async function analyzeRow(row) {

    if (row.dataset.phishingChecking === "true") {
        return;
    }

    if (
        row.querySelector(
            ".latvian-phishing-bubble"
        )
    ) {
        return;
    }

    row.dataset.phishingChecking = "true";


    // Получаем весь видимый текст строки
    const text = row.innerText.trim();

    if (!text) {
        return;
    }


    // Получаем элементы темы/preview
    const subjectElement =
        row.querySelector(".bog");

    const previewElement =
        row.querySelector(".y2");


    let subject = "";
    let message = "";


    if (subjectElement) {
        subject =
            subjectElement.innerText.trim();
    }


    if (previewElement) {
        message =
            previewElement.innerText.trim();
    }


    // Если Gmail не дал отдельные элементы,
    // используем весь текст строки
    if (!subject && !message) {

        message = text;
    }


    try {

        const response = await fetch(
            API_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    subject: subject,
                    message: message
                })
            }
        );


        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const data = await response.json();

        const probability =
            Number(data.phishing_probability);


        console.log(
            "Latvian Email Security:",
            probability,
            subject
        );


        // <25% — ничего
        if (probability < 25) {
            return;
        }


        const bubble =
            createBubble(probability);


        if (!bubble) {
            return;
        }


        // Ищем последнюю ячейку строки
        const cells =
            row.querySelectorAll("td");


        if (cells.length === 0) {
            return;
        }


        const lastCell =
            cells[cells.length - 1];


        lastCell.style.whiteSpace =
            "nowrap";


        lastCell.appendChild(bubble);


    } catch (error) {

        console.error(
            "Latvian Email Security error:",
            error
        );
    }
}


// ==========================================
// Поиск писем
// ==========================================

function scanEmails() {

    const rows =
        document.querySelectorAll("tr.zA");


    console.log(
        "Atrastas vēstuļu rindas:",
        rows.length
    );


    rows.forEach(row => {

        analyzeRow(row);

    });
}


// ==========================================
// Запускаем сканирование
// ==========================================

scanEmails();


// ==========================================
// Следим за Gmail
// ==========================================

const observer =
    new MutationObserver(() => {

        scanEmails();

    });


observer.observe(
    document.body,
    {
        childList: true,
        subtree: true
    }
);