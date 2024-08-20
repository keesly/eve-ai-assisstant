// src/main.js
import { createApp } from 'vue';
import App from './App.vue';

import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faArrowUp } from '@fortawesome/free-solid-svg-icons'; // Import the arrow-up icon

// Add the arrow-up icon to the library
library.add(faArrowUp);

// Register the FontAwesomeIcon component globally
const app = createApp(App);
app.component('font-awesome-icon', FontAwesomeIcon);

// Mount the Vue instance
app.mount('#app');
