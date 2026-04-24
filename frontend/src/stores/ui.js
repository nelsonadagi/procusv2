import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUIStore = defineStore('ui', () => {
  const isChatOpen = ref(false);
  const activeChatRoomId = ref(null);

  function openChat(roomId) {
    activeChatRoomId.value = roomId;
    isChatOpen.value = true;
  }

  function closeChat() {
    isChatOpen.value = false;
    activeChatRoomId.value = null;
  }

  return {
    isChatOpen,
    activeChatRoomId,
    openChat,
    closeChat
  };
});
