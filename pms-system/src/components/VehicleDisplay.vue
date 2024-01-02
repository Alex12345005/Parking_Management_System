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
          <td style="color: black">{{ vehicle.UsersID }}</td>
          <td style="color: black">{{ vehicle.LicensePlate }}</td>
          <td style="color: black">{{ vehicle.TagID }}</td>
          <td style="color: black">{{ vehicle.PermissionID }}</td>
          <td style="color: black">{{ vehicle.StartTime }}</td>
          <td style="color: black">{{ vehicle.EndTime }}</td>
          <td><button class="uk-button uk-button-default" type="button" uk-toggle="target: #offcanvas-flip">Open</button>
            <div id="offcanvas-flip" uk-offcanvas="flip: true; overlay: true">
                <div class="uk-offcanvas-bar">
                    <button class="uk-offcanvas-close" type="button" uk-close></button>
                    <h3>Title</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
                </div>
            </div>
          </td>
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
  TagID: number; 
  PermissionID: number; 
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
