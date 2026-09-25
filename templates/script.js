const API_URL = "http://127.0.0.1:8000";

const queryInput = document.getElementById("queryInput");
const sendButton = document.getElementById("sendButton");
const chatContainer = document.getElementById("chatContainer");

const fileInput = document.getElementById("fileInput");
const dropZone = document.getElementById("dropZone");

const documentList = document.getElementById("documentList");
const documentCount = document.getElementById("documentCount");

const welcomeScreen = document.getElementById("welcomeScreen");

const notification = document.getElementById("notification");

let documents = [];


/* ================= NOTIFICATION ================= */

function showNotification(message) {

    notification.textContent = message;

    notification.classList.add("show");

    setTimeout(() => {
        notification.classList.remove("show");
    }, 3000);
}


/* ================= DOCUMENT UPLOAD ================= */

fileInput.addEventListener("change", () => {

    if (fileInput.files.length > 0) {

        uploadFile(fileInput.files[0]);

    }

});


async function uploadFile(file) {

    showNotification(`Uploading ${file.name}...`);

    addDocument(file.name, "Uploading...");

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch(
            `${API_URL}/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Upload failed"
            );

        }

        updateDocumentStatus(
            file.name,
            "Indexed"
        );

        showNotification(
            `${file.name} indexed successfully`
        );

    } catch (error) {

        updateDocumentStatus(
            file.name,
            "Failed"
        );

        showNotification(
            `Upload failed: ${error.message}`
        );

        console.error(error);
    }
}


/* ================= DRAG & DROP ================= */

dropZone.addEventListener(
    "dragover",
    (event) => {

        event.preventDefault();

        dropZone.style.color = "#9d92ff";

    }
);


dropZone.addEventListener(
    "dragleave",
    () => {

        dropZone.style.color = "";

    }
);


dropZone.addEventListener(
    "drop",
    (event) => {

        event.preventDefault();

        dropZone.style.color = "";

        const files = event.dataTransfer.files;

        if (files.length > 0) {

            uploadFile(files[0]);

        }

    }
);


/* ================= DOCUMENT LIST ================= */

function addDocument(name, status) {

    const existing = documents.find(
        doc => doc.name === name
    );

    if (existing) {

        existing.status = status;

        renderDocuments();

        return;
    }

    documents.push({
        name: name,
        status: status
    });

    renderDocuments();
}


function updateDocumentStatus(name, status) {

    const document = documents.find(
        doc => doc.name === name
    );

    if (document) {

        document.status = status;

    }

    renderDocuments();
}


function renderDocuments() {

    documentCount.textContent = documents.length;

    if (documents.length === 0) {

        documentList.innerHTML = `
            <div class="empty-documents">
                No documents uploaded yet
            </div>
        `;

        return;
    }

    documentList.innerHTML = "";

    documents.forEach(doc => {

        const item = document.createElement("div");

        item.className = "document-item";

        let statusClass = "";

        if (doc.status === "Indexed") {
            statusClass = "indexed";
        }

        item.innerHTML = `
            <div class="document-icon">
                📄
            </div>

            <div class="document-info">

                <div class="document-name">
                    ${escapeHtml(doc.name)}
                </div>

                <div class="document-status ${statusClass}">
                    ${escapeHtml(doc.status)}
                </div>

            </div>
        `;

        documentList.appendChild(item);

    });
}


/* ================= CHAT ================= */

async function sendMessage() {

    const query = queryInput.value.trim();

    if (!query) {
        return;
    }

    welcomeScreen.style.display = "none";

    addMessage(
        query,
        "user"
    );

    queryInput.value = "";

    autoResize();

    sendButton.disabled = true;

    const typingId = showTyping();

    try {

        const response = await fetch(
            `${API_URL}/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    query: query
                })
            }
        );

        const data = await response.json();

        removeTyping(typingId);

        if (!response.ok) {

            throw new Error(
                data.detail || "Chat request failed"
            );

        }

        addAIMessage(
            data.answer,
            data.sources
        );

    } catch (error) {

        removeTyping(typingId);

        addAIMessage(
            `Something went wrong: ${error.message}`,
            []
        );

        console.error(error);

    } finally {

        sendButton.disabled = false;

        queryInput.focus();

    }
}


/* ================= ADD USER MESSAGE ================= */

function addMessage(text, type) {

    const message = document.createElement("div");

    message.className =
        `message ${type}-message`;

    message.innerHTML = `
        <div class="message-content">
            ${escapeHtml(text)}
        </div>
    `;

    chatContainer.appendChild(message);

    scrollToBottom();
}


/* ================= ADD AI MESSAGE ================= */

function addAIMessage(answer, sources) {

    const message = document.createElement("div");

    message.className =
        "message ai-message";

    let sourcesHTML = "";

    if (sources && sources.length > 0) {

        sourcesHTML = `
            <div class="sources">

                ${sources.map(source => `

                    <div class="source-card">

                        <strong>
                            📄 ${escapeHtml(
                                source.source.split("/").pop()
                            )}
                        </strong>

                        <br>

                        ${escapeHtml(
                            source.type
                        )}

                        · Page
                        ${escapeHtml(
                            String(source.page_no)
                        )}

                    </div>

                `).join("")}

            </div>
        `;
    }

    message.innerHTML = `

        <div class="message-content">

            ${formatAnswer(answer)}

            ${sourcesHTML}

        </div>

    `;

    chatContainer.appendChild(message);

    scrollToBottom();
}


/* ================= TYPING INDICATOR ================= */

function showTyping() {

    const id =
        "typing-" + Date.now();

    const message =
        document.createElement("div");

    message.id = id;

    message.className =
        "message ai-message";

    message.innerHTML = `

        <div class="message-content typing">

            <span></span>
            <span></span>
            <span></span>

        </div>

    `;

    chatContainer.appendChild(message);

    scrollToBottom();

    return id;
}


function removeTyping(id) {

    const element =
        document.getElementById(id);

    if (element) {

        element.remove();

    }
}


/* ================= SUGGESTIONS ================= */

function useSuggestion(text) {

    queryInput.value = text;

    autoResize();

    queryInput.focus();

}


/* ================= NEW CHAT ================= */

function newChat() {

    chatContainer.innerHTML = "";

    chatContainer.appendChild(
        welcomeScreen
    );

    welcomeScreen.style.display = "";

}


/* ================= TEXTAREA ================= */

queryInput.addEventListener(
    "input",
    autoResize
);


queryInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


function autoResize() {

    queryInput.style.height = "auto";

    queryInput.style.height =
        Math.min(
            queryInput.scrollHeight,
            130
        ) + "px";

}


/* ================= HELPERS ================= */

function scrollToBottom() {

    chatContainer.scrollTop =
        chatContainer.scrollHeight;
}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


function formatAnswer(text) {

    return escapeHtml(text)
        .replace(/\n/g, "<br>");
}