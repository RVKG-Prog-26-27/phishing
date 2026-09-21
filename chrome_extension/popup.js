document.getElementById("analyze").addEventListener("click", async () => {

    const resultElement = document.getElementById("result");

    resultElement.textContent = "Iegūstam e-pastu...";

    try {

        const tabs = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        const tab = tabs[0];

        if (!tab.url || !tab.url.includes("mail.google.com")) {
            resultElement.textContent =
                "Lūdzu, atver Gmail un izvēlies e-pastu.";
            return;
        }

        const emailData = await chrome.scripting.executeScript({
            target: {
                tabId: tab.id
            },

            func: () => {

                // Atrodam e-pasta tēmu
                let subject = "";

                const subjectSelectors = [
                    "h2.hP",
                    "h2[data-thread-perm-id]",
                    "[role='main'] h2"
                ];

                for (const selector of subjectSelectors) {

                    const element =
                        document.querySelector(selector);

                    if (element && element.innerText.trim()) {
                        subject = element.innerText.trim();
                        break;
                    }
                }


                // Atrodam e-pasta tekstu
                let message = "";

                const messageSelectors = [
                    ".a3s.aiL",
                    ".a3s",
                    "[role='main'] .ii.gt",
                    "[role='main'] .gs"
                ];

                for (const selector of messageSelectors) {

                    const elements =
                        document.querySelectorAll(selector);

                    for (const element of elements) {

                        const text =
                            element.innerText.trim();

                        if (text.length > message.length) {
                            message = text;
                        }
                    }
                }


                // Rezultāts
                return {
                    subject: subject,
                    message: message
                };
            }
        });


        const email = emailData[0].result;


        if (!email.subject && !email.message) {

            resultElement.innerHTML = `
                <p><b>Neizdevās nolasīt e-pastu.</b></p>
                <p>
                    Pārliecinies, ka Gmail ir atvērta
                    konkrēta vēstule.
                </p>
            `;

            return;
        }


        resultElement.textContent =
            "Analizējam e-pastu...";


        const response = await fetch(
            "http://127.0.0.1:5000/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    subject: email.subject,
                    message: email.message
                })
            }
        );


        if (!response.ok) {
            throw new Error(
                `Server error: ${response.status}`
            );
        }


        const data = await response.json();


        resultElement.innerHTML = `
            <p>
                <b>Tēma:</b>
                ${email.subject || "Nav atrasta"}
            </p>

            <p>
                <b>Rezultāts:</b>
                ${data.prediction}
            </p>

            <p>
                <b>Phishing:</b>
                ${data.phishing_probability}%
            </p>

            <p>
                <b>Normal:</b>
                ${data.normal_probability}%
            </p>

            <p>
                <b>Bīstams:</b>
                ${data.dangerous}
            </p>

            <p>
                <b>Draudu pazīmes:</b>
            </p>

            <ul>
                ${
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
});