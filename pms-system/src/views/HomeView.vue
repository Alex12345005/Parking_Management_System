<!-- HomeView.vue -->

<template>
  <div class="home-view">
    <div class="content-section">
      <VehicleDisplay />
      <PostVehicle />
    </div>
  </div>
</template>

<script setup lang="ts">
import VehicleDisplay from '../components/VehicleDisplay.vue';
import PostVehicle from '../components/PostVehicle.vue';

const handleLogout = () => {
  localStorage.removeItem('access_token');
  window.location.reload();
}
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.divider {
  width: 50%;
  margin: 10px 0;
  border: 1px solid #000;
}

.content-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
