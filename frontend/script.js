const API_URL = "";

const chat = document.getElementById("chat");
const question = document.getElementById("question");
const sendButton = document.getElementById("send");


function addMessage(text, type) {

    const message = document.createElement("div");

    message.className = "message " + type;

    const content = document.createElement("div");

    content.className = "message-content";

    content.textContent = text;

    message.appendChild(content);

    chat.appendChild(message);

    chat.scrollTop = chat.scrollHeight;
}


async function askAI() {

    const text = question.value.trim();

    if (!text) {
        return;
    }

    addMessage(text, "user");

    question.value = "";

    sendButton.disabled = true;
    sendButton.textContent = "...";

    try {

        const response = await fetch(API_URL + "/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: text
            })

        });


        if (!response.ok) {
            throw new Error("API request failed");
        }


        const data = await response.json();

        addMessage(data.answer, "ai");


    } catch (error) {

        console.error(error);

        addMessage(
            "Sorry, I couldn't connect to SivoAI. Please check that the SivoAI server and Ollama are running.",
            "ai"
        );

    } finally {

        sendButton.disabled = false;
        sendButton.textContent = "Send";

        question.focus();
    }
}


/* Send button */

sendButton.addEventListener("click", askAI);


/* Enter to send */

question.addEventListener("keydown", function(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        askAI();

    }

});