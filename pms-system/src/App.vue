<!-- app.vue -->

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import VehicleDisplay from './components/VehicleDisplay.vue'

const handleLogout = () => {
  localStorage.removeItem('access_token');
  window.location.reload();
}
</script>

<template>
  <div>
    <div class="menu-button-wrapper">
      <button class="uk-button uk-button-secondary uk-border-rounded uk-margin-small-right" type="button" uk-toggle="target: #offcanvas-nav-primary">Nav</button>
    </div>
    <div id="offcanvas-slide" uk-offcanvas></div>
    <div id="offcanvas-nav-primary" uk-offcanvas="overlay: true">
      <div class="uk-offcanvas-bar uk-flex uk-flex-column">
        <ul class="uk-nav uk-nav-primary uk-nav-center uk-margin-auto-vertical">
          <li class="uk-active"><span uk-icon="home"></span><RouterLink to="/" class="link-text">Home</RouterLink></li>
          <li class="uk-active"><span uk-icon="info"></span><RouterLink to="/about" class="link-text">About</RouterLink></li>
          <li class="uk-nav-divider"></li>
          <li><a href="#" @click.prevent="handleLogout" class="link-text">Logout</a></li>
        </ul>
      </div>
    </div>
    <div class="uk-container-expand">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
@media (min-width: 1024px) {
  header {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 20px;
    margin: 0 auto;
  }
  .menu-button-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    margin: 1rem;
  }
  .link-text {
    color: black;
    font-size: 18px; 
  }

  .uk-button-secondary {
    background-color: black;
    color: white;
    font-size: 18px; 
  }

  .uk-button-secondary.uk-border-rounded {
    border-radius: 10px;
  }
}
</style>
