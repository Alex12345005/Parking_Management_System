<template>
  <div>
    <h2>Vehicle Table</h2>
    <table class="uk-table uk-table-large uk-table-hover uk-table-divider vehicle-table-justify">
      <thead>
        <tr>
          <th>Vehicle ID</th>
          <th>User ID</th>
          <th>License Plate</th>
          <th>Tag ID</th>
          <th>Permission ID</th>
          <th>Start Time</th>
          <th>End Time</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(vehicle, index) in vehicles" :key="index" class="uk-background-muted">
          <td style="color: black">{{ vehicle.VehicleID }}</td>
          <td style="color: black">{{ vehicle.UsersID }}</td> <!-- Update property name to UsersID -->
          <td style="color: black">{{ vehicle.LicensePlate }}</td>
          <td style="color: black">{{ vehicle.TagID }}</td>
          <td style="color: black">{{ vehicle.PermissionID }}</td>
          <td style="color: black">{{ vehicle.StartTime }}</td>
          <td style="color: black">{{ vehicle.EndTime }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

interface Vehicle {
  VehicleID: number;
  UsersID: number;
  LicensePlate: string;
  TagID: number; // Add TagID
  PermissionID: number; // Add PermissionID
  StartTime: string;
  EndTime: string;
}

const vehicles = ref<Vehicle[]>([]);
const isEditPopupVisible = ref(false);
const editedVehicle = ref<Vehicle | null>(null);

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/vehicles/get_vehicles/', {
      withCredentials: true,
    });
    vehicles.value = response.data;
    console.log('API Response:', response.data);
  } catch (error) {
    console.error('Error fetching vehicle data:', error);
  }
});
</script>

<style scoped>

</style>
