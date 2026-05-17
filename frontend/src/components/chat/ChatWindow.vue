<template>
  <div class="c-chat-interface" :class="{ 'c-chat-interface--dark': isDarkMode }">
    <!-- Sidebar (Contact List) -->
    <aside class="c-chat-sidebar" :class="{ 'c-chat-sidebar--collapsed': isSidebarCollapsed }">
      <div class="c-chat-sidebar__header">
        <div class="c-user-profile">
          <div class="c-avatar c-avatar--md">
            <span class="c-avatar__initials">{{ userInitials }}</span>
            <span class="c-status-dot c-status-dot--online"></span>
          </div>
          <div class="c-user-profile__info" v-if="!isSidebarCollapsed">
            <h3 class="c-user-profile__name">My Account</h3>
            <span class="c-user-profile__status">Secure Connection</span>
          </div>
        </div>
        <button class="c-icon-btn" @click="toggleSidebar" title="Toggle Sidebar">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="9" y1="3" x2="9" y2="21"/></svg>
        </button>
      </div>

      <div class="c-chat-search" v-if="!isSidebarCollapsed">
        <div class="c-input-icon-wrapper">
          <svg class="c-input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" placeholder="Search encrypted chats..." class="c-input c-input--sm c-input--dark">
        </div>
      </div>

      <div class="c-chat-list" v-if="!isSidebarCollapsed">
        <h4 class="c-chat-list__title">Recent Secure Chats</h4>
        <div 
          v-for="room in chatRooms" 
          :key="room.id" 
          class="c-chat-item" 
          :class="{ 'c-chat-item--active': room.id === roomId }"
          @click="$emit('select-room', room.id)"
        >
          <div class="c-avatar">
            <span class="c-avatar__initials">{{ getInitials(room.name) }}</span>
          </div>
          <div class="c-chat-item__content">
            <div class="c-chat-item__top">
              <span class="c-chat-item__name">{{ room.name }}</span>
              <span class="c-chat-item__time">{{ formatTime(room.last_message_at) }}</span>
            </div>
            <div class="c-chat-item__preview">
              <svg v-if="room.is_encrypted" class="c-lock-icon-xs" xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              {{ room.last_message || 'Start a secure conversation' }}
            </div>
          </div>
        </div>
        <!-- Mock Item if list empty -->
        <div v-if="chatRooms.length === 0" class="c-chat-item c-chat-item--active">
           <div class="c-avatar"><span class="c-avatar__initials">#</span></div>
           <div class="c-chat-item__content">
             <div class="c-chat-item__top"><span class="c-chat-item__name">Current Chat</span></div>
             <div class="c-chat-item__preview">Active Session</div>
           </div>
        </div>
      </div>
    </aside>

    <!-- Main Chat Area -->
    <main class="c-chat-main">
      <!-- Header -->
      <header class="c-chat-header">
        <div class="c-chat-header__info">
          <div class="c-avatar">
            <span class="c-avatar__initials">#</span>
          </div>
          <div class="c-chat-header__details">
            <h2 class="c-chat-header__title">
              Room #{{ roomId }}
              <span class="c-badge c-badge--success c-badge--pill">
                <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                E2EE Active
              </span>
            </h2>
            <span class="c-chat-header__status">
              <span class="c-status-indicator" :class="connectionStatusClass"></span>
              {{ connectionStatusText }}
              <span v-if="isTyping" class="c-typing-indicator-text"> • Someone is typing...</span>
            </span>
          </div>
        </div>
        <div class="c-chat-header__actions">
          <button class="c-icon-btn" title="Search Message"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>
          <button class="c-icon-btn" title="Secure Verification"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></button>
          <button class="c-icon-btn" title="Settings"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg></button>
        </div>
      </header>

      <!-- Messages Area -->
      <div class="c-messages-area" ref="messagesContainer">
        <div class="c-encryption-notice">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          Messages are end-to-end encrypted. No one outside of this chat, not even Procus, can read or listen to them.
        </div>
        
        <div v-for="(group, date) in groupedMessages" :key="date" class="c-message-group">
          <div class="c-date-divider"><span>{{ formatDateLabel(date) }}</span></div>
          
          <div 
            v-for="message in group" 
            :key="message.message_id" 
            class="c-message"
            :class="{ 'c-message--own': isOwnMessage(message) }"
          >
            <div class="c-message__bubble">
              <div v-if="!isOwnMessage(message)" class="c-message__sender">{{ message.sender_username }}</div>
              
              <div v-if="message.attachment" class="c-attachment-card">
                 <template v-if="message.attachment.file_type && message.attachment.file_type.startsWith('image/')">
                    <img :src="message.attachment.file_url" class="c-attachment-img" alt="Image" loading="lazy" />
                 </template>
                 <template v-else>
                    <div class="c-file-attachment">
                      <div class="c-file-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>
                      </div>
                      <div class="c-file-info">
                        <span class="c-file-name">{{ getFileName(message.attachment.file_url) }}</span>
                        <a :href="message.attachment.file_url" target="_blank" class="c-file-link">Download</a>
                      </div>
                    </div>
                 </template>
              </div>

              <div class="c-message__text">{{ message.content }}</div>
              
              <div class="c-message__meta">
                <span class="c-message__time">{{ formatTime(message.timestamp) }}</span>
                <span v-if="isOwnMessage(message)" class="c-message__status">
                  <!-- Double check icon for read (mock logic) -->
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="c-icon-check"><polyline points="20 6 9 17 4 12"/></svg>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="c-input-area">
        <div v-if="selectedFile" class="c-file-preview">
          <div class="c-file-preview__card">
             <span class="c-file-preview__icon">📎</span>
             <span class="c-file-preview__name">{{ selectedFile.name }}</span>
             <button class="c-file-preview__remove" @click="selectedFile = null">×</button>
          </div>
        </div>
        
        <div class="c-input-bar">
          <button class="c-icon-btn" @click="triggerFileInput" title="Attach File">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
          </button>
          <input type="file" ref="fileInput" @change="handleFileChange" hidden />
          
          <div class="c-input-wrapper">
             <textarea 
               v-model="currentMessage" 
               @keydown.enter.exact.prevent="sendMessage"
               placeholder="Type a secure message..." 
               class="c-chat-input"
               rows="1"
               @input="adjustHeight"
             ></textarea>
          </div>

          <button class="c-send-btn" @click="sendMessage" :disabled="!canSend">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </div>
        <div class="c-input-footer">
           <span class="c-secure-badge"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg> Encrypted</span>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue';
import api from '../../services/api';

const props = defineProps({
  roomId: { type: String, required: true },
});

// State
const messages = ref([]);
const currentMessage = ref('');
const messagesContainer = ref(null);
const fileInput = ref(null);
const webSocket = ref(null);
const selectedFile = ref(null);
const isSidebarCollapsed = ref(false);
const chatRooms = ref([]); // Mock or fetch
const currentUser = ref({ username: 'You' }); // Replaced by logic
const isTyping = ref(false);
const wsStatus = ref('connecting'); // connecting, open, closed, error
const isDarkMode = ref(false); // Can be toggled

// Computed
const canSend = computed(() => currentMessage.value.trim() !== '' || selectedFile.value);
const connectionStatusText = computed(() => {
    switch(wsStatus.value) {
        case 'open': return 'Securely Connected';
        case 'connecting': return 'Establishing Secure Channel...';
        case 'closed': return 'Disconnected';
        default: return 'Connection Error';
    }
});
const connectionStatusClass = computed(() => {
    switch(wsStatus.value) {
        case 'open': return 'c-status-indicator--online';
        case 'connecting': return 'c-status-indicator--connecting';
        default: return 'c-status-indicator--offline';
    }
});
const userInitials = computed(() => 'ME'); // Placeholder

// Group messages by date
const groupedMessages = computed(() => {
    const groups = {};
    messages.value.forEach(msg => {
        const date = new Date(msg.timestamp).toLocaleDateString();
        if (!groups[date]) groups[date] = [];
        groups[date].push(msg);
    });
    return groups;
});

// Helpers
const isOwnMessage = (msg) => msg.sender_username === currentUser.value.username;
const formatTime = (iso) => new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
const formatDateLabel = (dateStr) => {
    const date = new Date(dateStr);
    const today = new Date().toLocaleDateString();
    return dateStr === today ? 'Today' : dateStr;
};
const getInitials = (name) => name ? name.substring(0, 2).toUpperCase() : '#';
const getFileName = (url) => url.split('/').pop();
const toggleSidebar = () => isSidebarCollapsed.value = !isSidebarCollapsed.value;
const triggerFileInput = () => fileInput.value.click();
const adjustHeight = (e) => {
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
};

// Logic
const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
};

const uploadAttachment = async () => {
  if (!selectedFile.value) return null;
  const formData = new FormData();
  formData.append('file', selectedFile.value);
  formData.append('message', 'Attachment'); 
  try {
    const response = await api.post('/chat/attachments/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  } catch (error) {
    console.error('Upload failed:', error);
    return null;
  }
};

const sendMessage = async () => {
  if (!canSend.value) return;

  const messagePayload = {
    message: currentMessage.value,
    attachment_id: null,
  };

  if (selectedFile.value) {
    const attachmentData = await uploadAttachment();
    if (attachmentData) {
      messagePayload.attachment_id = attachmentData.id;
    } else {
      return; // Error handled in uploadAttachment
    }
  }

  if (webSocket.value && webSocket.value.readyState === WebSocket.OPEN) {
    webSocket.value.send(JSON.stringify(messagePayload));
    currentMessage.value = '';
    selectedFile.value = null;
  }
};

const fetchHistoricalMessages = async () => {
  try {
    const response = await api.get(`/chat/rooms/${props.roomId}/messages/`);
    messages.value = response.data;
    scrollToBottom();
  } catch (error) {
    console.error('Failed to fetch messages:', error);
  }
};

const scrollToBottom = () => {
    nextTick(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
      }
    });
};

onMounted(() => {
  // Try to get user info from local storage
  const userStr = localStorage.getItem('user'); // Assuming stored as JSON
  if (userStr) {
      try { currentUser.value = JSON.parse(userStr); } catch(e) {}
  }

  fetchHistoricalMessages();

  const token = localStorage.getItem('token');
  
  if (token) {
      const explicitWsUrl = import.meta.env.VITE_WS_URL;
      let wsUrl;
      if (explicitWsUrl) {
        const url = new URL(explicitWsUrl);
        url.pathname = `/ws/chat/${props.roomId}/`;
        url.searchParams.set('token', token);
        wsUrl = url.toString();
      } else {
        const fallbackApi = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
          ? `${window.location.protocol}//${window.location.hostname}:8007/api`
          : `${window.location.origin}/api`;
        const apiBase = import.meta.env.VITE_API_URL || fallbackApi;
        const apiUrl = new URL(apiBase, window.location.origin);
        const protocol = apiUrl.protocol === 'https:' ? 'wss:' : 'ws:';
        wsUrl = `${protocol}//${apiUrl.host}/ws/chat/${props.roomId}/?token=${token}`;
      }
      webSocket.value = new WebSocket(wsUrl);

      webSocket.value.onopen = () => { wsStatus.value = 'open'; };
      webSocket.value.onclose = () => { wsStatus.value = 'closed'; };
      webSocket.value.onerror = () => { wsStatus.value = 'error'; };
      
      webSocket.value.onmessage = (event) => {
        const data = JSON.parse(event.data);
        messages.value.push(data);
        scrollToBottom();
      };
  }
});

onUnmounted(() => {
  if (webSocket.value) webSocket.value.close();
});
</script>

<style scoped>
/* Scoped Layout Styles */
.c-chat-interface {
  display: flex;
  height: 600px;
  max-height: 80vh;
  width: 100%;
  background-color: var(--color-bg-card, #fff);
  border-radius: var(--radius-xl, 12px);
  box-shadow: var(--shadow-xl, 0 20px 25px -5px rgba(0,0,0,0.1));
  overflow: hidden;
  font-family: var(--font-sans, sans-serif);
  border: 1px solid var(--color-border, #eaecf0);
}

/* Sidebar */
.c-chat-sidebar {
  width: 280px;
  background-color: #0f172a; /* Deep Slate */
  color: white;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #1e293b;
  transition: width 0.3s ease;
}

.c-chat-sidebar--collapsed {
  width: 60px;
}

.c-chat-sidebar__header {
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #1e293b;
  height: 64px;
}

.c-user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  overflow: hidden;
}

.c-user-profile__info {
  white-space: nowrap;
}

.c-user-profile__name {
  font-size: 14px;
  font-weight: 600;
  margin: 0;
}

.c-user-profile__status {
  font-size: 11px;
  color: #94a3b8;
  display: block;
}

.c-chat-search {
  padding: 12px;
}

.c-input-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.c-input-icon {
  position: absolute;
  left: 10px;
  color: #64748b;
}

.c-input--dark {
  background: #1e293b;
  border: 1px solid #334155;
  color: white;
  padding-left: 36px;
  border-radius: 6px;
  width: 100%;
  font-size: 13px;
}

.c-input--dark:focus {
  border-color: #38bdf8;
  outline: none;
}

.c-chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px 0;
}

.c-chat-list__title {
  padding: 0 16px 8px;
  font-size: 11px;
  text-transform: uppercase;
  color: #64748b;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.c-chat-item {
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: background 0.2s;
}

.c-chat-item:hover {
  background: rgba(255,255,255,0.05);
}

.c-chat-item--active {
  background: rgba(56, 189, 248, 0.1); /* Primary hint */
  border-left: 3px solid #38bdf8;
}

.c-chat-item__content {
  flex: 1;
  overflow: hidden;
}

.c-chat-item__top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2px;
}

.c-chat-item__name {
  font-size: 13px;
  font-weight: 600;
  color: #e2e8f0;
}

.c-chat-item__time {
  font-size: 11px;
  color: #64748b;
}

.c-chat-item__preview {
  font-size: 12px;
  color: #94a3b8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Main Area */
.c-chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc; /* neutral-50 */
}

/* Header */
.c-chat-header {
  height: 64px;
  background: white;
  border-bottom: 1px solid var(--color-border, #eaecf0);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.c-chat-header__info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.c-chat-header__title {
  font-size: 16px;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.c-chat-header__status {
  font-size: 12px;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 6px;
}

.c-status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ccc;
}
.c-status-indicator--online { background: #10b981; box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2); }
.c-status-indicator--offline { background: #ef4444; }
.c-status-indicator--connecting { background: #f59e0b; }

.c-chat-header__actions {
  display: flex;
  gap: 8px;
}

/* Messages */
.c-messages-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-image: radial-gradient(#e2e8f0 1px, transparent 1px);
  background-size: 20px 20px;
}

.c-encryption-notice {
  text-align: center;
  font-size: 11px;
  color: #64748b;
  background: #f1f5f9;
  border-radius: 8px;
  padding: 8px 12px;
  margin: 0 auto 20px;
  max-width: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.c-date-divider {
  text-align: center;
  margin: 20px 0;
  position: relative;
}

.c-date-divider span {
  background: #e2e8f0;
  color: #475467;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 12px;
}

.c-message {
  display: flex;
  margin-bottom: 12px;
}

.c-message--own {
  justify-content: flex-end;
}

.c-message__bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 12px;
  position: relative;
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #e2e8f0;
}

.c-message--own .c-message__bubble {
  background: #e0f2fe; /* primary-100 */
  border-color: #bae6fd;
  border-bottom-right-radius: 2px;
}

.c-message:not(.c-message--own) .c-message__bubble {
  border-bottom-left-radius: 2px;
}

.c-message__sender {
  font-size: 11px;
  font-weight: 700;
  color: #0369a1; /* primary-700 */
  margin-bottom: 4px;
}

.c-message__text {
  font-size: 14px;
  color: #1e293b;
  line-height: 1.5;
  word-break: break-word;
}

.c-message__meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
  margin-top: 4px;
}

.c-message__time {
  font-size: 10px;
  color: #94a3b8;
}

.c-message__status {
  color: #3b82f6; /* Blue checks */
  display: flex;
}

/* Attachments */
.c-attachment-card {
  margin-bottom: 8px;
}

.c-attachment-img {
  max-width: 200px;
  border-radius: 8px;
  border: 1px solid rgba(0,0,0,0.1);
}

.c-file-attachment {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(0,0,0,0.03);
  padding: 8px;
  border-radius: 8px;
}

.c-file-info {
  display: flex;
  flex-direction: column;
}

.c-file-name {
  font-size: 12px;
  font-weight: 600;
}

.c-file-link {
  font-size: 11px;
  color: #0284c7;
  text-decoration: none;
}

/* Input Area */
.c-input-area {
  background: white;
  border-top: 1px solid var(--color-border, #eaecf0);
  padding: 16px 20px;
}

.c-file-preview {
  margin-bottom: 10px;
}

.c-file-preview__card {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f1f5f9;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
}

.c-file-preview__remove {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  font-weight: bold;
}

.c-input-bar {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.c-input-wrapper {
  flex: 1;
  position: relative;
}

.c-chat-input {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 20px;
  padding: 10px 16px;
  font-size: 14px;
  resize: none;
  max-height: 120px;
  font-family: inherit;
  background: #f8fafc;
}

.c-chat-input:focus {
  outline: none;
  background: white;
  border-color: #38bdf8;
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.1);
}

.c-icon-btn {
  background: none;
  border: none;
  color: #64748b;
  padding: 8px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.c-icon-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.c-send-btn {
  background: #0284c7; /* primary-600 */
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(2, 132, 199, 0.3);
  transition: transform 0.1s;
}

.c-send-btn:hover {
  background: #0369a1;
}

.c-send-btn:active {
  transform: scale(0.95);
}

.c-send-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
  box-shadow: none;
}

.c-input-footer {
  text-align: center;
  margin-top: 8px;
}

.c-secure-badge {
  font-size: 10px;
  color: #94a3b8;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

/* Avatar Utilities */
.c-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 13px;
  position: relative;
  flex-shrink: 0;
}

.c-avatar--md {
  width: 40px;
  height: 40px;
}

.c-status-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid #0f172a; /* matches sidebar bg */
}
.c-status-dot--online { background: #10b981; }

</style>
