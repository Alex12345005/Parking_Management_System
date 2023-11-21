<template>
  <div>
    <h2>Vehicle Table</h2>
    <table>
      <thead>
        <tr>
          <th>Vehicle ID</th>
          <th>Owner Name</th>
          <th>License Plate</th>
          <th>Created At</th>
          <th>Updated At</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="vehicle in vehicles" :key="vehicle.vehicle_id">
          <td>{{ vehicle.vehicle_id }}</td>
          <td>{{ vehicle.owner_name }}</td>
          <td>{{ vehicle.license_plate }}</td>
          <td>{{ vehicle.created_at }}</td>
          <td>{{ vehicle.updated_at }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

interface Vehicle {
  vehicle_id: number;
  owner_name: string;
  license_plate: string;
  created_at: string;
  updated_at: string;
}

const vehicles = ref<Vehicle[]>([]);

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/vehicles/get_vehicle/', {
      withCredentials: true,  // Enable sending credentials (cookies, headers) in cross-origin requests
    });
    vehicles.value = response.data;
  } catch (error) {
    console.error('Error fetching vehicle data:', error);
  }
});
</script>
