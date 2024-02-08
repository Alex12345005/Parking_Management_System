<template>
  <div class="vehicle-display-container">
    <div class="scrollable-table-container">
      <table class="uk-table uk-table-hover uk-table-divider vehicle-table-justify uk-background-default">
        <thead class="sticky-header">
          <tr>
            <th style="color: black">Vehicle ID</th>
            <th style="color: black">User ID</th>
            <th style="color: black">License Plate</th>
            <th style="color: black">Tag ID</th>
            <th style="color: black">Permission ID</th>
            <th style="color: black">Start Time</th>
            <th style="color: black">End Time</th>
            <th style="color: black">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(vehicle, index) in vehicles" :key="index">
            <td style="color: black">{{ vehicle.VehicleID }}</td>
            <td style="color: black">{{ vehicle.UsersID }}</td>
            <td style="color: black">{{ vehicle.LicensePlate }}</td>
            <td style="color: black">{{ vehicle.TagID }}</td>
            <td style="color: black">{{ vehicle.PermissionID }}</td>
            <td style="color: black">{{ vehicle.StartTime }}</td>
            <td style="color: black">{{ vehicle.EndTime }}</td>
            <td><button class="uk-button uk-button-default" type="button" uk-toggle="target: #offcanvas-flip">✏️</button>
              <div id="offcanvas-flip" uk-offcanvas="flip: true; overlay: true">
                  <div class="uk-offcanvas-bar">
                      <button class="uk-offcanvas-close" type="button" uk-close></button>
                      <h3>Edit Vehicle</h3>
                      <form @submit.prevent="postVehicle">
                        <div class="form-group">
                          <label for="userDropdown">Users:</label>
                          <select v-model="userId" id="userDropdown" class="uk-select" required>
                            <option value="">Select a User</option>
                            <option v-for="user in users" :key="user.UserID" :value="user.UserID">{{ user.Username }}</option>
                          </select>
                        </div>

                        <div class="form-group">
                          <label for="licensePlate">License Plate:</label>
                          <input v-model="licensePlate" type="text" id="licensePlate" class="uk-input" required />
                        </div>

                        <div class="form-group">
                          <label for="startTime">Start Time:</label>
                          <input v-model="startTime" type="datetime-local" id="startTime" class="uk-input" required />
                        </div>

                        <div class="form-group">
                          <label for="endTime">End Time:</label>
                          <input v-model="endTime" type="datetime-local" id="endTime" class="uk-input" required />
                        </div>

                      
                        <div class="form-group">
                          <label for="tagDropdown">Tag:</label>
                          <select v-model="tagId" id="tagDropdown" class="uk-select" required>
                            <option value="">Select a Tag</option>
                            <option v-for="tag in tags" :key="tag.TagID" :value="tag.TagID">{{ tag.TagName }}</option>
                          </select>
                        </div>

                        <div class="form-group">
                          <label for="parkingPermissions">Parking Permissions:</label>
                          <div>
                            <div v-for="(permission, index) in parkingPermissions" :key="permission.PermissionType">
                              <input
                                @input="updateSelectedPermissions(permission.PermissionID)"
                                type="checkbox"
                                :id="'permission' + permission.PermissionType"
                                :value="permission.PermissionType"
                                name="parkingPermission"
                              />
                              <label :for="'permission' + permission.PermissionType">{{ permission.PermissionType }}</label>
                            </div>
                          </div>
                        </div>

                        <button type="submit" class="uk-button uk-button-primary uk-button-small">
                          <span uk-icon="plus"></span> Update Vehicle
                        </button>
                      </form>
                      <button class="uk-button uk-button-default" style="margin-top: 10px;" @click="deleteVehicle(vehicle.VehicleID)">Delete 🗑️</button>
                  </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
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
  TagID: number;
  PermissionID: number[];
  StartTime: string;
  EndTime: string;
}

const vehicles = ref<Vehicle[]>([]);

onMounted(async () => {
  await fetchVehicles();
});

async function fetchVehicles() {
  try {
    const response = await axios.get('http://localhost:8000/vehicles/get_vehicles/', {
      withCredentials: true,
    });
    vehicles.value = response.data;
  } catch (error) {
    console.error('Error fetching vehicle data:', error);
  }
}

async function deleteVehicle(vehicleId: number) {
  const isConfirmed = confirm(`Are you sure you want to delete the vehicle with ID ${vehicleId}?`);

  if (isConfirmed) {
    try {
      await axios.delete(`http://localhost:8000/vehicles/delete_vehicle/${vehicleId}`, {
        withCredentials: true,
      });
      await fetchVehicles(); // Fahrzeuge neu laden, um die Liste zu aktualisieren
      alert(`Vehicle with ID ${vehicleId} has been deleted.`);
    } catch (error) {
      console.error('Error deleting vehicle:', error);
      alert('Failed to delete vehicle.');
    }
  }
}
</script>

<style scoped>
.scrollable-table-container {
  overflow-y: auto;
  max-height: 750px; /* Anpassen nach Bedarf */
}

.sticky-header th {
  position: sticky;
  top: 0;
  background-color: #fff; /* Hintergrund des Headers */
  z-index: 1; /* Stellt sicher, dass der Header über den Zeilen bleibt */
}

/* Optional: Schatten oder Linie, um den Header hervorzuheben */
.sticky-header th::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  border-bottom: 2px solid #ccc; /* Linie unter dem Header */
}
</style>