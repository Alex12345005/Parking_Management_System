<template>
  <div>
    <h2>Vehicle Table</h2>
    <table class="vehicle-table">
      <thead>
        <tr>
          <th>Vehicle ID</th>
          <th>Owner Name</th>
          <th>License Plate</th>
          <th>Created At</th>
          <th>Updated At</th>
          <th>Action</th> <!-- New column for edit buttons -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="vehicle in vehicles" :key="vehicle.vehicle_id">
          <td>{{ vehicle.vehicle_id }}</td>
          <td>{{ vehicle.owner_name }}</td>
          <td>{{ vehicle.license_plate }}</td>
          <td>{{ vehicle.created_at }}</td>
          <td>{{ vehicle.updated_at }}</td>
          <td>
            <button @click="openEditPopup(vehicle)">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Popup for editing -->
    <div v-if="isEditPopupVisible" class="popup">
      <form @submit.prevent="editVehicle">
        <!-- Editable fields -->
        <div class="form-group">
          <label for="editOwnerName">Owner Name:</label>
          <input v-model="editedVehicle.owner_name" type="text" id="editOwnerName" required />
        </div>
        <div class="form-group">
          <label for="editLicensePlate">License Plate:</label>
          <input v-model="editedVehicle.license_plate" type="text" id="editLicensePlate" required />
        </div>

        <!-- Delete button within the popup -->
        <button type="button" @click="confirmDelete">Delete</button>

        <!-- Confirmation before saving changes -->
        <button type="submit">Save Changes</button>
        <button type="button" @click="cancelEdit">Cancel</button>
      </form>
    </div>
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
    // If successful, update the list of vehicles
    vehicles.value = vehicles.value.filter(vehicle => vehicle.vehicle_id !== vehicleId);
    // Close the popup after deletion
    isEditPopupVisible.value = false;
  } catch (error) {
    console.error(`Error deleting vehicle with ID ${vehicleId}:`, error);
  }
};

const openEditPopup = (vehicle: Vehicle) => {
  editedVehicle.value = { ...vehicle };
  isEditPopupVisible.value = true;
};

const confirmDelete = () => {
  const isConfirmed = window.confirm('Are you sure you want to delete this vehicle?');
  if (isConfirmed) {
    deleteVehicle(editedVehicle.value?.vehicle_id || 0);
  }
};

const editVehicle = () => {
  // Implement your edit logic here
  // ...

  // Close the popup after editing
  isEditPopupVisible.value = false;
};

const cancelEdit = () => {
  // Reset edited data
  editedVehicle.value = null;
  // Close the popup
  isEditPopupVisible.value = false;
};
</script>


<style scoped>
.vehicle-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.vehicle-table th, .vehicle-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.vehicle-table th {
  background-color: #ff8c00; /* Orange background color */
  color: white; /* Text color */
  font-weight: bold; /* Bold text */
}

.vehicle-table tbody tr:nth-child(even) {
  background-color: black;
}
</style>

