<!-- HomeView.vue -->

<template>
  <div>
    <h1>Welcome to the Home View!</h1>
    <VehicleDisplay />
    <PostVehicle />
  </div>
  <button
    id="logout-button"
    @click.prevent="handleLogout"
  >
    Log out
  </button>
</template>

<script setup lang="ts">
import VehicleDisplay from '../components/VehicleDisplay.vue';
import PostVehicle from '../components/PostVehicle.vue';

const handleLogout = () => {
  localStorage.removeItem('access_token');
  window.location.reload();
}
</script>
