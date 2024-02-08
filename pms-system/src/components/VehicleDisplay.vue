<template>
  <div>
    <h2>Vehicle Table</h2>
    <table class="uk-table uk-table-large uk-table-hover uk-table-divider vehicle-table-justify uk-background-tertiary">
      <thead>
        <tr>
          <th style="color: black">Vehicle ID</th>
          <th style="color: black">User ID</th>
          <th style="color: black">License Plate</th>
          <th style="color: black">Tag ID</th>
          <th style="color: black">Permission ID</th>
          <th style="color: black">Start Time</th>
          <th style="color: black">End Time</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(vehicle, index) in vehicles" :key="index" class="uk-background-default">
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
.uk-background-tertiary{
    background-color: #d3d3d3; 
}
</style>
