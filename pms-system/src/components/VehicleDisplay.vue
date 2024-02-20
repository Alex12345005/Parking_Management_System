<template>
  <div class="vehicle-display-container">
    <div class="scrollable-table-container">
      <table class="uk-table uk-table-hover uk-table-divider vehicle-table-justify uk-background-default">
        <thead class="sticky-header">
          <tr>
            <th style="color: black; font-weight: bold; font-size: 18px;">Vehicle ID</th>
            <th style="color: black; font-weight: bold; font-size: 18px;">User ID</th>
            <th style="color: black; font-weight: bold; font-size: 18px;">License Plate</th>
            <th style="color: black; font-weight: bold; font-size: 18px;">Tag ID</th>
            <th style="color: black; font-weight: bold; font-size: 18px;">Permission ID</th>
            <th style="color: black; font-weight: bold; font-size: 18px;">Start Time</th>
            <th style="color: black; font-weight: bold; font-size: 18px;">End Time</th>
            <th style="color: black; font-weight: bold; font-size: 18px;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(vehicle, index) in vehicles" :key="index">
            <td style="font-size: 16px; color: black">{{ vehicle.VehicleID }}</td>
            <td style="font-size: 16px; color: black">{{ vehicle.UsersID }}</td>
            <td style="font-size: 16px; color: black">{{ vehicle.LicensePlate }}</td>
            <td style="font-size: 16px; color: black">{{ vehicle.TagID }}</td>
            <td style="font-size: 16px; color: black">{{ vehicle.PermissionID }}</td>
            <td style="font-size: 16px; color: black">{{ vehicle.StartTime }}</td>
            <td style="font-size: 16px; color: black">{{ vehicle.EndTime }}</td>
            <td style="font-size: 16px; color: black"><button class="uk-button uk-button-default" type="button" @click="openEditModal(vehicle)">✏️</button></td>
          </tr>
        </tbody>
      </table>
    </div>
<!-- Edit Modal -->
<div id="editVehicleModal" uk-modal>
      <div class="uk-modal-dialog">
        <button class="uk-modal-close-default" type="button" uk-close></button>
        <div class="uk-modal-header">
          <h2 class="uk-modal-title">Edit Vehicle</h2>
        </div>
        <div class="uk-modal-body">
          <!-- Formular für Bearbeitung -->
          <div class="form-group">
            <label for="userDropdown">Users:</label>
            <select v-model="editingVehicle.UsersID" id="userDropdown" class="uk-select" required>
              <option v-for="user in users" :key="user.UserID" :value="user.UserID">{{ user.Username }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="licensePlate">License Plate:</label>
            <input v-model="editingVehicle.LicensePlate" type="text" id="licensePlate" class="uk-input" required />
          </div>
          <div class="form-group">
            <label for="startTime">Start Time:</label>
            <input v-model="editingVehicle.StartTime" type="datetime-local" id="startTime" class="uk-input" required />
          </div>
          <div class="form-group">
            <label for="endTime">End Time:</label>
            <input v-model="editingVehicle.EndTime" type="datetime-local" id="endTime" class="uk-input" required />
          </div>
          <div class="form-group">
            <label for="tagDropdown">Tag:</label>
            <select v-model="editingVehicle.TagID" id="tagDropdown" class="uk-select" required>
              <option v-for="tag in tags" :key="tag.TagID" :value="tag.TagID">{{ tag.TagName }}</option>
            </select>
          </div>
        </div>
        <div class="uk-modal-footer custom-modal-footer">
          <button class="uk-button uk-button-danger" @click="deleteVehicle(editingVehicle.VehicleID)">Delete</button>
          <div class="button-group-right">
            <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
            <button class="uk-button uk-button-primary" @click="updateVehicle">Save Changes</button>
          </div>
        </div>
      </div>
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

const users = ref([]);
const tags = ref([]);
const parkingPermissions = ref([]);
const vehicles = ref<Vehicle[]>([]);

onMounted(async () => {
  await fetchVehicles();
  await loadUsers();
  await loadTags();
  await loadParkingPermissions();
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
      await fetchVehicles(); 
      alert(`Vehicle with ID ${vehicleId} has been deleted.`);
    } catch (error) {
      console.error('Error deleting vehicle:', error);
      alert('Failed to delete vehicle.');
    }
  }
}

async function loadUsers() {
  try {
    const response = await axios.get('http://localhost:8000/users/get_users/');
    users.value = response.data;
  } catch (error) {
    console.error('Error loading users:', error);
  }
}

async function loadTags() {
  try {
    const response = await axios.get('http://localhost:8000/tags/get_tags/');
    tags.value = response.data;
  } catch (error) {
    console.error('Error loading tags:', error);
  }
}

async function loadParkingPermissions() {
  try {
    const response = await axios.get('http://localhost:8000/parking_permissions/get_parking_permissions/');
    parkingPermissions.value = response.data;
  } catch (error) {
    console.error('Error loading parking permissions:', error);
  }
}

const editingVehicle = ref({} as Vehicle | null);

function openEditModal(vehicle) {
  editingVehicle.value = { ...vehicle };
  UIkit.modal("#editVehicleModal").show();
}

async function updateVehicle() {
  if (!editingVehicle.value) return;
  
  // Stellen Sie sicher, dass die VehicleID vorhanden ist
  const vehicleId = editingVehicle.value.VehicleID;
  if (!vehicleId) {
    alert('Vehicle ID is missing');
    return;
  }

  const updateUrl = `http://localhost:8000/vehicles/update_vehicles/${vehicleId}`;
  
  try {
    const response = await axios.put(updateUrl, {
      // Achten Sie darauf, dass die Struktur hier der erwarteten Struktur entspricht
      VehicleID: editingVehicle.value.VehicleID,
      LicensePlate: editingVehicle.value.LicensePlate,
      UsersID: editingVehicle.value.UsersID,
      TagID: editingVehicle.value.TagID,
      PermissionID: editingVehicle.value.PermissionID,
      StartTime: editingVehicle.value.StartTime,
      EndTime: editingVehicle.value.EndTime,
    }, {
      withCredentials: true,
    });

    // Verarbeiten Sie hier die Antwort
    await fetchVehicles(); // Aktualisieren Sie die Liste der Fahrzeuge
    UIkit.modal("#editVehicleModal").hide();
    alert('Vehicle updated successfully');
  } catch (error) {
    console.error('Error updating vehicle:', error);
    alert(`Failed to update vehicle: ${error.message}`);
  }
}
</script>

<style scoped>
.uk-table th, .uk-table td {
  padding: 10px 20px; 
  text-align: left;
  border-right: 1px solid #ccc; 
}

.uk-table th:last-child, .uk-table td:last-child {
  border-right: none;
}

.scrollable-table-container {
  overflow-y: auto;
  max-height: 750px; 
}

.sticky-header th {
  position: sticky;
  top: 0;
  background-color: #fff; 
  z-index: 2; 
}

.sticky-header th::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  border-bottom: 2px solid #ccc; 
}

.uk-modal-dialog {
  color: black; /* Setzt die Standardtextfarbe im gesamten Modal auf Schwarz */
}

.uk-select, .uk-input {
  color: black; /* Stellt sicher, dass die Textfarbe in Formularelementen ebenfalls Schwarz ist */
}

/* Optional: Falls Sie spezifische Textelemente haben, die angepasst werden müssen */
.uk-modal-title, label {
  color: black; /* Stellt sicher, dass Titel und Labels im Modal Schwarz sind */
}

.custom-modal-footer {
  display: flex;
  justify-content: space-between; /* Platziert Elemente an den gegenüberliegenden Enden des Containers */
  align-items: center; /* Zentriert die Buttons vertikal */
}

.button-group-right {
  display: flex;
  gap: 10px; /* Fügt einen Abstand zwischen den Buttons hinzu */
}
</style>