<template>
  <div id="app" style="height: 100%; position: relative;">
    <router-view />
    <ChatBot class="chatbot-overlay" />
  </div>
</template>

<script>
import ChatBot from './components/ChatBot.vue'

export default {
    name: 'App',
    components: {
        ChatBot
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Nunito+Sans&display=swap');

#app {
    font-family: 'Nunito Sans', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

html,
body {
    overscroll-behavior-y: contain;
}

.chatbot-overlay {
    position: absolute;
    bottom: 20px;
    right: 20px;
    width: 380px;
    z-index: 1000;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
    background: white;
    border-radius: 10px;
}
</style>
