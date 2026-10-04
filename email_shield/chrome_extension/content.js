console.log("Latvian Email Security: scanner started");


const API_URL = "http://127.0.0.1:5000/analyze";



const analysisCache = new Map();




function getEmailId(row) {

    const attributes = [
        "data-legacy-thread-id",
        "data-thread-id",
        "data-legacy-message-id"
    ];


    for (const attribute of attributes) {

        const value =
            row.getAttribute(attribute);

        if (value) {
            return attribute + ":" + value;
        }
    }


    const elementWithId =
        row.querySelector(
            "[data-legacy-thread-id], " +
            "[data-thread-id], " +
            "[data-legacy-message-id]"
        );


    if (elementWithId) {

        for (const attribute of attributes) {

            const value =
                elementWithId.getAttribute(attribute);

            if (value) {
                return attribute + ":" + value;
            }
        }
    }


    const text =
        row.innerText
            .replace(/\s+/g, " ")
            .trim();


    return "text:" + text;
}




function createBubble(category) {

    const bubble =
        document.createElement("span");


    bubble.className =
        "latvian-email-category";


    let text = "";
    let backgroundColor = "";


    // NORMAL
    if (category === "normal") {

        text = "NORMAL";
        backgroundColor = "#16a34a";

    }


    // ADVERTISING
    else if (category === "advertising") {

        text = "ADVERTISING";
        backgroundColor = "#2563eb";

    }


    // SPAM
    else if (category === "spam") {

        text = "SPAM";
        backgroundColor = "#f59e0b";

    }


    // PHISHING
    else if (category === "phishing") {

        text = "PHISHING";
        backgroundColor = "#dc2626";

    }


    // Неизвестная категория
    else {

        text = category.toUpperCase();
        backgroundColor = "#6b7280";
    }


    bubble.textContent = text;


    bubble.style.display =
        "inline-flex";

    bubble.style.alignItems =
        "center";

    bubble.style.justifyContent =
        "center";


    bubble.style.height =
        "26px";


    bubble.style.padding =
        "0 10px";


    bubble.style.marginLeft =
        "10px";


    bubble.style.borderRadius =
        "14px";


    bubble.style.color =
        "white";


    bubble.style.backgroundColor =
        backgroundColor;


    bubble.style.fontSize =
        "11px";


    bubble.style.fontWeight =
        "bold";


    bubble.style.fontFamily =
        "Arial, sans-serif";


    bubble.style.verticalAlign =
        "middle";


    bubble.style.position =
        "relative";


    bubble.style.zIndex =
        "999999";


    bubble.title =
        "Kategorija: " + text;


    return bubble;
}




function showBubble(row, category) {

    if (!category) {
        return;
    }


    // Если уже есть категория
    if (
        row.querySelector(
            ".latvian-email-category"
        )
    ) {
        return;
    }


    const bubble =
        createBubble(category);


    const cells =
        row.querySelectorAll("td");


    if (cells.length === 0) {
        return;
    }


    const lastCell =
        cells[cells.length - 1];


    lastCell.style.whiteSpace =
        "nowrap";


    lastCell.appendChild(
        bubble
    );
}




async function analyzeRow(row) {

    const emailId =
        getEmailId(row);


    

    if (analysisCache.has(emailId)) {

        const category =
            analysisCache.get(emailId);


        showBubble(
            row,
            category
        );


        return;
    }


    

    if (
        row.dataset.lesAnalyzing === "true"
    ) {
        return;
    }


    row.dataset.lesAnalyzing =
        "true";


    const text =
        row.innerText
            .replace(/\s+/g, " ")
            .trim();


    if (!text) {

        delete row.dataset.lesAnalyzing;

        return;
    }


    console.log(
        "Analizējam:",
        text.substring(0, 120)
    );


    try {

        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        subject: "",
                        message: text
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        const category =
            data.category ||
            data.prediction;


        console.log(
            "Kategorija:",
            category
        );


        

        analysisCache.set(
            emailId,
            category
        );


        

        showBubble(
            row,
            category
        );


    } catch (error) {

        console.error(
            "Latvian Email Security:",
            error
        );

    } finally {

        delete row.dataset.lesAnalyzing;
    }
}




function scanEmails() {

    const rows =
        document.querySelectorAll(
            "tr.zA"
        );


    console.log(
        "Atrastas vēstuļu rindas:",
        rows.length
    );


    rows.forEach(
        row => {
            analyzeRow(row);
        }
    );
}




scanEmails();




let scanTimeout = null;


const observer =
    new MutationObserver(() => {

        if (scanTimeout) {

            clearTimeout(
                scanTimeout
            );
        }


        scanTimeout =
            setTimeout(() => {

                scanEmails();

            }, 300);
    });


observer.observe(
    document.body,
    {
        childList: true,
        subtree: true
    }
);




setInterval(() => {

    scanEmails();

}, 2000);