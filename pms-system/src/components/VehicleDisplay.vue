<template>
  <div>
    <h2>Vehicle Table</h2>
    <table class="uk-table uk-table-large uk-table-hover uk-table-divider vehicle-table-justify">
      <thead>
        <tr>
          <th>Vehicle ID</th>
          <th>User ID</th>
          <th>License Plate</th>
          <th>Start Time</th>
          <th>End Time</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(vehicle, index) in vehicles" :key="index" class="uk-background-muted" @click="selectRow(vehicle)">
          <!-- Use uk-table-link class and uk-link-reset for clickable cells -->
          <td class="uk-table-link uk-link-reset">{{ vehicle.VehicleID }}</td>
          <td class="uk-table-link uk-link-reset">{{ vehicle.UsersID }}</td>
          <td class="uk-table-link uk-link-reset">{{ vehicle.LicensePlate }}</td>
          <td class="uk-table-link uk-link-reset">{{ vehicle.StartTime }}</td>
          <td class="uk-table-link uk-link-reset">{{ vehicle.EndTime }}</td>
          <td>
            <button @click="openEditPopup(vehicle)" class="uk-button uk-button-default uk-button-small">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Popup for editing -->
    <div v-if="isEditPopupVisible" class="popup uk-padding-small">
      <form @submit.prevent="editVehicle">
        <div class="form-group">
          <label for="editLicensePlate">License Plate:</label>
          <!-- Update the v-model based on the new model -->
          <input v-model="editedVehicle.LicensePlate" type="text" id="editLicensePlate" class="uk-input" required />
        </div>

        <!-- Add other form fields based on the new model -->

        <button type="submit" class="uk-button uk-button-primary uk-button-small">Save Changes</button>
        <button type="button" @click="cancelEdit" class="uk-button uk-button-secondary uk-button-small">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

interface Vehicle {
  VehicleID: number;
  UsersID: number;
  LicensePlate: string;
  StartTime: string;
  EndTime: string;
}

const vehicles = ref<Vehicle[]>([]);
const isEditPopupVisible = ref(false);
const editedVehicle = ref<Vehicle | null>(null);

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/vehicles/get_vehicle/', {
      withCredentials: true,
    });
    vehicles.value = response.data;
  } catch (error) {
    console.error('Error fetching vehicle data:', error);
  }
});

const deleteVehicle = async (vehicleId: number) => {
  try {
    await axios.delete(`http://localhost:8000/vehicles/delete_vehicle/${vehicleId}`);
    vehicles.value = vehicles.value.filter(vehicle => vehicle.VehicleID !== vehicleId);
    isEditPopupVisible.value = false;
  } catch (error) {
    console.error(`Error deleting vehicle with ID ${vehicleId}:`, error);
  }
};

const openEditPopup = (vehicle: Vehicle) => {
  editedVehicle.value = { ...vehicle };
  isEditPopupVisible.value = true;
};

const selectRow = (vehicle: Vehicle) => {
  // Handle row selection logic here (e.g., highlighting the selected row)
  openEditPopup(vehicle);
};

const confirmDelete = () => {
  const isConfirmed = window.confirm('Are you sure you want to delete this vehicle?');
  if (isConfirmed) {
    deleteVehicle(editedVehicle.value?.VehicleID || 0);
  }
};

const editVehicle = () => {
  // Implement your edit logic here
  // ...

  isEditPopupVisible.value = false;
};

const cancelEdit = () => {
  editedVehicle.value = null;
  isEditPopupVisible.value = false;
};
</script>

<style scoped>
.popup {
  padding: 20px;
}

/* Add a style for highlighting the selected row */
.vehicle-table-justify tbody tr.selected {
  background-color: #e0e0e0;
}
</style>
