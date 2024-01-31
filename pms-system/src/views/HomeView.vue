<!-- HomeView.vue -->

<template>
  <div class="home-view">
    <h1 class="uk-heading-divider uk-position-top-center">Welcome to the PM-System</h1>
    <div class="content-section">
      <div class="chart-wrapper">
        <div class="flex-container">
        <VehicleDisplay />
        <PostVehicle />
      </div>
      </div>
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
  min-height: 70vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.content-section {
  display: flex;
  justify-content: center;
  align-items: flex-start; /* Align the items to the top of the container */
}

.flex-container {
  display: flex;
  flex-direction: row; /* Horizontal arrangement */
}

.chart-wrapper {
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
  gap: 2rem;
  padding: 3rem;
  padding-right: 0rem;
  background-color: #f5f5f5;
  margin-right: 0px;
}
</style>