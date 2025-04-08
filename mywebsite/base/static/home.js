
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

chatSocket.onopen = function () {
    console.log("The connection was set up successfully!");
};

function formatTime(time) {
    let date;
    try {
        date = new Date(time);
            if (isNaN(date)) {
            const [hours, minutes] = time.split(":").map(Number);
            if (!isNaN(hours) && !isNaN(minutes)) {
                return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
            }
            throw new Error("Invalid time format");
        }
    } catch (error) {
        console.error("Invalid time format:", time);
        return "Invalid Time";
    }
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

let lastId = 0;
async function loadMessages() {
    try {
        const response = await fetch(`/api/load_messages/?last_id=${lastId}`);

        if (!response.ok) throw new Error(`Failed to load messages: ${response.statusText}`);
    
        const data = await response.json();
        const messageContainer = document.getElementById('id_chat_item_container');
    
        data.messages.forEach(msg => {
            const messageDiv = document.createElement('div');
    
            const messageClass = msg.sender === "{{ request.user.username }}" ? "chat-message right" : "chat-message left";
    
            messageDiv.className = messageClass;
            messageDiv.innerHTML = `
                <div class="message-content">
                    <span class="message-username">${msg.sender}</span>
                    <span class="message-text">${msg.message}</span>
                    <span class="message-timestamp">${formatTime(msg.timestamp)}</span>
                </div>
            `;
            messageContainer.appendChild(messageDiv);
        });
    
        messageContainer.scrollTop = messageContainer.scrollHeight;
    } catch (error) {
        console.error('Error loading messages:', error);
    }
} 

loadMessages();

chatSocket.onclose = function () {
    console.log("Connection closed.");
};

chatSocket.onerror = function (error) {
    console.error("WebSocket error:", error);
};

document.getElementById('messageButton').addEventListener('click', function () {
    document.getElementById('chatMenu').style.display = 'block';
});

document.getElementById('closeChatButton').addEventListener('click', function () {
    document.getElementById('chatMenu').style.display = 'none';
});

document.querySelector("#id_message_send_input").onkeyup = function (e) {
    if (e.keyCode === 13) {
        document.querySelector("#id_message_send_button").click();
    }
};

document.querySelector("#id_message_send_button").onclick = function () {
    const messageInput = document.querySelector("#id_message_send_input").value;
    const currentTime = new Date();
    const time = currentTime.toLocaleTimeString();

    chatSocket.send(JSON.stringify({
        message: messageInput,
        username: "{{ request.user.username }}",
        time: time
    }));

    document.querySelector("#id_message_send_input").value = "";
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const messageContainer = document.querySelector("#id_chat_item_container");
    const div = document.createElement("div");
    
    const formattedTime = formatTime(data.time);
    
    div.className = (data.username === "{{ request.user.username }}") ? "chat-message right" : "chat-message left";
    div.innerHTML = `<div class="message-content">
        <span class="message-username">${data.username}</span>
        <span class="message-text">${data.message}</span>
        <span class="message-timestamp">${formattedTime}</span>
    </div>`;
    messageContainer.appendChild(div);
    messageContainer.scrollTop = messageContainer.scrollHeight;
};

    
let lastProfileId = 0;

    function loadProfiles() {
        fetch(`/api/load_profiles/?last_id=${lastProfileId}`)
            .then(response => response.json())
            .then(data => {
                const feed = document.getElementById('feed');
                data.profiles.forEach(profile => {
                    const profileCard = document.createElement('div');
                    profileCard.className = 'main-card';
                    profileCard.innerHTML = `
                        <img src="${profile.photo}" alt="Profile Photo" style="width:100%; border-radius: 10px; margin-bottom: 10px;">
                        <h2>
                            <a href="/profile/${profile.username}" style="color: #fff; text-decoration: none;">
                                ${profile.username}
                            </a>
                        </h2>  
                        <p>Age: ${profile.age}</p>
                        <p>Bio: ${profile.bio}</p> 
                        <button class="like-button" data-profile-id="${profile.id}">Like</button>
                        <button class="dislike-button" data-profile-id="${profile.id}">Dislike</button>
                    `;

                    feed.appendChild(profileCard);
                    lastProfileId = profile.id;
                });
            })
            .catch(error => console.error('Error loading profiles:', error));
    }
    const rightPanel = document.querySelector('.right-panel');
    rightPanel.addEventListener('scroll', () => {
        if (rightPanel.scrollTop + rightPanel.clientHeight >= rightPanel.scrollHeight) {
            loadProfiles();
        }
    });

    document.addEventListener('DOMContentLoaded', () => {
        loadProfiles();
    });

    document.getElementById('matchMenu').addEventListener('click', function () {
        document.getElementById('matchesMenu').style.display = 'block';
    });

    document.getElementById('closeMatchButton').addEventListener('click', function () {
        document.getElementById('matchesMenu').style.display = 'none';
    });   