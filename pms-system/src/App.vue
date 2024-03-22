<!-- app.vue -->

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'

const handleLogout = () => {
  localStorage.removeItem('access_token');
  window.location.reload();
}
</script>

<template>
  <div class="app-container">
    <nav class="sidebar">
      <ul class="uk-nav uk-nav-primary uk-nav-center uk-margin-auto-vertical">
        <li class="uk-active"><span uk-icon="home"></span><RouterLink to="/" class="link-text">Home</RouterLink></li>
        <li class="uk-active"><span uk-icon="info"></span><RouterLink to="/about" class="link-text">About</RouterLink></li>
        <li class="uk-nav-divider"></li>
        <li><a href="#" @click.prevent="handleLogout" class="link-text">Logout</a></li>
      </ul>
    </nav>
    <div class="main-content">
      <RouterView />
    </div>
  </div>
</template>

<style>
.app-container {
  display: flex;
}

.sidebar {
  display: flex; /* Use flexbox for layout */
  flex-direction: column; /* Stack items vertically */
  justify-content: center; /* Center items vertically */
  align-items: center; /* Center items horizontally */
  width: 250px; /* Adjust the width of the sidebar as needed */
  height: 100vh; /* Full height of the viewport */
  position: fixed; /* Fixed position */
  left: 0; /* Stick to the left */
  top: 0; /* Stick to the top */
  overflow-y: auto; /* Enable vertical scrolling if necessary */
  background-color: #282828;
  color: white;
}

.main-content {
  margin-left: 0px; /* Adjust this value to reduce the gap */
  flex-grow: 1;
}

.sidebar .uk-nav-primary li a,
.sidebar .uk-nav-primary li a:link,
.sidebar .uk-nav-primary li a:visited,
.sidebar .uk-nav-primary li a:hover,
.sidebar .uk-nav-primary li a:active,
.sidebar .uk-nav-primary li a:focus {
  color: white !important; /* This will force the text color to be white */
  font-size: 20px;
}

/* Additional styling and responsive design as needed */
</style>
