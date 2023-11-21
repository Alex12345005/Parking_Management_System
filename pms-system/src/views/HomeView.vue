<!-- HomeView.vue -->

<template>
  <div>
    <h1>Welcome to the Home View!</h1>
    <VehicleDisplay />
    <PostVehicle />
  </div>
</template>

<script setup lang="ts">
import VehicleDisplay from '../components/VehicleDisplay.vue';
import PostVehicle from '../components/PostVehicle.vue';
</script>
