document.addEventListener("DOMContentLoaded", () => {

const chat = document.getElementById("chat");
const input = document.getElementById("question");
const button = document.getElementById("askBtn");

button.addEventListener("click", ask);

// Handle ask button
input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        ask();
    }
});
// Add message to chat
function addMessage(text, cls) {
    const div = document.createElement("div");
    div.className = `message ${cls}`;
    div.innerHTML = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return div;
}

// Streaming chat response
async function ask() {
    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");

    input.value = "";
    button.disabled = true;

    const botMsg = addMessage("", "bot");

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    let buffer = "";
    let contexts = [];
    let confidence = 0;

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        const parts = buffer.split("\n\n");
        buffer = parts.pop();

        for (let part of parts) {

            if (part.startsWith("event: done")) {
                const meta = JSON.parse(part.split("data: ")[1]);
                contexts = meta.contexts;
                confidence = meta.confidence;
                continue;
            }

            if (part.startsWith("data: ")) {
                botMsg.innerHTML += part.replace("data: ", "");
                chat.scrollTop = chat.scrollHeight;
            }
        }
    }

    addSources(contexts, confidence);
    button.disabled = false;
    input.focus();
}

// Add sources with confidence score
function addSources(contexts, confidence) {
    const div = document.createElement("div");
    div.className = "message bot";

    div.innerHTML = `
    <details>
        <summary>Sources (confidence ${confidence.toFixed(2)})</summary>
        <pre style="white-space:pre-wrap">${contexts.join("\n\n---\n\n")}</pre>
    </details>
    `;

    chat.appendChild(div);
}


// Sidebar history
async function loadHistory() {
    const res = await fetch("/conversations");
    const chats = await res.json();

    const list = document.getElementById("historyList");
    list.innerHTML = "";

    chats.forEach(c => {
        const div = document.createElement("div");
        div.className = "chat-item";
        div.innerText = c.title;
        div.onclick = () => switchChat(c.id);
        list.appendChild(div);
    });
}
// Switch chat
async function switchChat(id) {
    await fetch(`/switch/${id}`);
    location.reload();
}
// New chat
async function newChat() {
    await fetch("/new");
    location.reload();
}

loadHistory();
});