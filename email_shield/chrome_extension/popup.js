document.getElementById("analyze").addEventListener(
    "click",
    async () => {

        const resultElement =
            document.getElementById("result");


        resultElement.textContent =
            "Iegūstam e-pastu...";


        try {

            // ======================================
            // Получаем текущую вкладку
            // ======================================

            const tabs =
                await chrome.tabs.query({
                    active: true,
                    currentWindow: true
                });


            const tab =
                tabs[0];


            if (
                !tab.url ||
                !tab.url.includes(
                    "mail.google.com"
                )
            ) {

                resultElement.textContent =
                    "Lūdzu, atver Gmail un izvēlies e-pastu.";

                return;
            }


            // ======================================
            // Получаем письмо из Gmail
            // ======================================

            const emailData =
                await chrome.scripting.executeScript({

                    target: {
                        tabId: tab.id
                    },


                    func: () => {

                        let subject = "";

                        const subjectSelectors = [

                            "h2.hP",

                            "h2[data-thread-perm-id]",

                            "[role='main'] h2"
                        ];


                        for (
                            const selector
                            of subjectSelectors
                        ) {

                            const element =
                                document.querySelector(
                                    selector
                                );


                            if (
                                element &&
                                element.innerText.trim()
                            ) {

                                subject =
                                    element.innerText.trim();

                                break;
                            }
                        }


                        let message = "";


                        const messageSelectors = [

                            ".a3s.aiL",

                            ".a3s",

                            "[role='main'] .ii.gt",

                            "[role='main'] .gs"
                        ];


                        for (
                            const selector
                            of messageSelectors
                        ) {

                            const elements =
                                document.querySelectorAll(
                                    selector
                                );


                            for (
                                const element
                                of elements
                            ) {

                                const text =
                                    element.innerText.trim();


                                if (
                                    text.length >
                                    message.length
                                ) {

                                    message =
                                        text;
                                }
                            }
                        }


                        return {
                            subject: subject,
                            message: message
                        };
                    }
                });


            const email =
                emailData[0].result;


            // ======================================
            // Проверяем письмо
            // ======================================

            if (
                !email.subject &&
                !email.message
            ) {

                resultElement.innerHTML = `

                    <p>
                        <b>Neizdevās nolasīt e-pastu.</b>
                    </p>

                    <p>
                        Pārliecinies, ka Gmail ir atvērta
                        konkrēta vēstule.
                    </p>

                `;

                return;
            }


            resultElement.textContent =
                "Analizējam e-pastu...";


            // ======================================
            // Отправляем письмо Python-серверу
            // ======================================

            const response =
                await fetch(
                    "http://127.0.0.1:5000/analyze",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            subject:
                                email.subject,

                            message:
                                email.message
                        })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `Server error: ${response.status}`
                );
            }


            const data =
                await response.json();


            // ======================================
            // Категория
            // ======================================

            const category =
                data.category ||
                data.prediction;


            let categoryText =
                category;


            if (
                category === "normal"
            ) {

                categoryText =
                    "NORMAL";

            } else if (
                category === "advertising"
            ) {

                categoryText =
                    "ADVERTISING";

            } else if (
                category === "spam"
            ) {

                categoryText =
                    "SPAM";

            } else if (
                category === "phishing"
            ) {

                categoryText =
                    "PHISHING";
            }


            // ======================================
            // Цвет категории
            // ======================================

            let categoryColor =
                "#6b7280";


            if (
                category === "normal"
            ) {

                categoryColor =
                    "#16a34a";

            } else if (
                category === "advertising"
            ) {

                categoryColor =
                    "#2563eb";

            } else if (
                category === "spam"
            ) {

                categoryColor =
                    "#f59e0b";

            } else if (
                category === "phishing"
            ) {

                categoryColor =
                    "#dc2626";
            }


            // ======================================
            // Показываем результат
            // ======================================

            resultElement.innerHTML = `

                <p>
                    <b>Tēma:</b>
                    ${email.subject || "Nav atrasta"}
                </p>

                <p>
                    <b>Kategorija:</b>

                    <span
                        style="
                            display:inline-block;
                            padding:5px 10px;
                            border-radius:12px;
                            background:${categoryColor};
                            color:white;
                            font-weight:bold;
                            font-size:12px;
                        "
                    >
                        ${categoryText}
                    </span>

                </p>

                <p>
                    <b>Draudu pazīmes:</b>
                </p>

                <ul>

                    ${
                        data.threats &&
                        data.threats.length > 0

                        ? data.threats
                            .map(
                                threat =>
                                    `<li>${threat}</li>`
                            )
                            .join("")

                        : "<li>Draudu pazīmes nav atrastas.</li>"
                    }

                </ul>

            `;


        } catch (error) {

            console.error(
                "Latvian Email Security:",
                error
            );


            resultElement.textContent =
                "Kļūda savienojumā ar Python serveri.";
        }

    }
);