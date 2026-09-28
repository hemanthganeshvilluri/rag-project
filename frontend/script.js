// FastAPI is inside Docker. Docker publishes container port 8000 to the host.
// Browser clients must use the host address, not 0.0.0.0.
const API_URL = "http://127.0.0.1:8000";

const queryInput=document.getElementById("queryInput");
const sendButton=document.getElementById("sendButton");
const chatContainer=document.getElementById("chatContainer");
const fileInput=document.getElementById("fileInput");
const browseButton=document.getElementById("browseButton");
const dropZone=document.getElementById("dropZone");
const documentList=document.getElementById("documentList");
const documentCount=document.getElementById("documentCount");
const welcomeScreen=document.getElementById("welcomeScreen");
const notification=document.getElementById("notification");
const newChatButton=document.getElementById("newChatButton");

let documents=[];
let notificationTimer=null;

function showNotification(message){
    notification.textContent=message;
    notification.classList.add("show");
    clearTimeout(notificationTimer);
    notificationTimer=setTimeout(()=>notification.classList.remove("show"),3000);
}

browseButton.addEventListener("click",()=>fileInput.click());

fileInput.addEventListener("change",()=>{
    if(fileInput.files.length){
        uploadFile(fileInput.files[0]);
        fileInput.value="";
    }
});

async function uploadFile(file){
    showNotification(`Uploading ${file.name}...`);
    addDocument(file.name,"Uploading...");

    const formData=new FormData();
    formData.append("file",file);

    try{
        const response=await fetch(`${API_URL}/upload`,{method:"POST",body:formData});
        const data=await readJson(response);
        if(!response.ok) throw new Error(data.detail||data.message||"Upload failed");
        updateDocumentStatus(file.name,"Indexed");
        showNotification(`${file.name} indexed successfully`);
    }catch(error){
        updateDocumentStatus(file.name,"Failed");
        showNotification(`Upload failed: ${error.message}`);
        console.error("Upload error:",error);
    }
}

dropZone.addEventListener("dragover",event=>{
    event.preventDefault();
    dropZone.classList.add("dragging");
});
dropZone.addEventListener("dragleave",()=>dropZone.classList.remove("dragging"));
dropZone.addEventListener("drop",event=>{
    event.preventDefault();
    dropZone.classList.remove("dragging");
    if(event.dataTransfer.files.length) uploadFile(event.dataTransfer.files[0]);
});

function addDocument(name,status){
    const existing=documents.find(doc=>doc.name===name);
    if(existing) existing.status=status;
    else documents.push({name,status});
    renderDocuments();
}

function updateDocumentStatus(name,status){
    const document=documents.find(doc=>doc.name===name);
    if(document) document.status=status;
    renderDocuments();
}

function renderDocuments(){
    documentCount.textContent=documents.length;

    if(!documents.length){
        documentList.innerHTML=`<div class="empty-documents"><span>◇</span><p>No documents yet</p><small>Upload a file to start asking questions.</small></div>`;
        return;
    }

    documentList.innerHTML="";
    documents.forEach(doc=>{
        const item=document.createElement("div");
        item.className="document-item";
        const statusClass=doc.status==="Indexed"?"indexed":doc.status==="Failed"?"failed":"";
        item.innerHTML=`
            <div class="document-icon">📄</div>
            <div class="document-info">
                <div class="document-name">${escapeHtml(doc.name)}</div>
                <div class="document-status ${statusClass}">${escapeHtml(doc.status)}</div>
            </div>`;
        documentList.appendChild(item);
    });
}

async function sendMessage(){
    const query=queryInput.value.trim();
    if(!query||sendButton.disabled) return;

    welcomeScreen.style.display="none";
    addMessage(query,"user");
    queryInput.value="";
    autoResize();
    sendButton.disabled=true;

    const typingId=showTyping();

    try{
        const response=await fetch(`${API_URL}/chat`,{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({query})
        });
        const data=await readJson(response);
        removeTyping(typingId);
        if(!response.ok) throw new Error(data.detail||data.message||"Chat request failed");
        addAIMessage(data.answer||"No answer returned.",data.sources||[]);
    }catch(error){
        removeTyping(typingId);
        addAIMessage(`Something went wrong: ${error.message}`,[]);
        console.error("Chat error:",error);
    }finally{
        sendButton.disabled=false;
        queryInput.focus();
    }
}

function addMessage(text,type){
    const message=document.createElement("div");
    message.className=`message ${type}-message`;
    message.innerHTML=`<div class="message-content">${escapeHtml(text).replace(/\n/g,"<br>")}</div>`;
    chatContainer.appendChild(message);
    scrollToBottom();
}

function addAIMessage(answer,sources){
    const message=document.createElement("div");
    message.className="message ai-message";

    let sourcesHTML="";
    if(sources.length){
        sourcesHTML=`<div class="sources">${sources.map(source=>{
            const fileName=source.source?source.source.split(/[\\/]/).pop():"Unknown source";
            const page=source.page_no??"N/A";
            const section=source.section??"N/A";
            const type=source.type??"unknown";
            return `<div class="source-card"><strong>📄 ${escapeHtml(fileName)}</strong><br>${escapeHtml(type)} · Section ${escapeHtml(String(section))} · Page ${escapeHtml(String(page))}</div>`;
        }).join("")}</div>`;
    }

    message.innerHTML=`<div class="message-content">${formatAnswer(answer)}${sourcesHTML}</div>`;
    chatContainer.appendChild(message);
    scrollToBottom();
}

function showTyping(){
    const id=`typing-${Date.now()}`;
    const message=document.createElement("div");
    message.className="message ai-message";
    message.id=id;
    message.innerHTML=`<div class="typing"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span><span style="margin-left:5px">Retrieving and generating...</span></div>`;
    chatContainer.appendChild(message);
    scrollToBottom();
    return id;
}

function removeTyping(id){
    const element=document.getElementById(id);
    if(element) element.remove();
}

function useSuggestion(text){
    queryInput.value=text;
    autoResize();
    queryInput.focus();
}

function newChat(){
    chatContainer.innerHTML="";
    chatContainer.appendChild(welcomeScreen);
    welcomeScreen.style.display="";
    queryInput.value="";
    autoResize();
    queryInput.focus();
}

newChatButton.addEventListener("click",newChat);
sendButton.addEventListener("click",sendMessage);
queryInput.addEventListener("input",autoResize);

queryInput.addEventListener("keydown",event=>{
    if(event.key==="Enter"&&!event.shiftKey){
        event.preventDefault();
        sendMessage();
    }
});

function autoResize(){
    queryInput.style.height="auto";
    queryInput.style.height=`${Math.min(queryInput.scrollHeight,130)}px`;
}

function scrollToBottom(){
    requestAnimationFrame(()=>chatContainer.scrollTop=chatContainer.scrollHeight);
}

function escapeHtml(text){
    return String(text)
        .replaceAll("&","&amp;")
        .replaceAll("<","&lt;")
        .replaceAll(">","&gt;")
        .replaceAll('"',"&quot;")
        .replaceAll("'","&#039;");
}

function formatAnswer(text){
    return escapeHtml(text).replace(/\n/g,"<br>").replace(/\*\*(.*?)\*\*/g,"<strong>$1</strong>");
}

async function readJson(response){
    const text=await response.text();
    if(!text) return {};
    try{return JSON.parse(text)}
    catch{return {detail:text||"Invalid response from server"}}
}

renderDocuments();
autoResize();
