<template>
  <div>
    <button @click="openOffCanvas" class="uk-button uk-button-secondary uk-margin-right uk-button-small">
      <a href="" uk-icon="plus"></a> Vehicle
    </button>

    <!-- Off-canvas panel -->
    <div id="offcanvas-usage" uk-offcanvas="flip: true">
      <div class="uk-offcanvas-bar">

        <!-- Close button for off-canvas panel -->
        <button class="uk-offcanvas-close" type="button" @click="closeOffCanvas"></button>

        <h3>Add Vehicle</h3>

        <!-- Form for adding a new vehicle -->
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
            <span uk-icon="plus"></span> Create new Vehicle
          </button>
        </form>
      </div>
    </div>

   
    <div v-if="feedbackMessage" class="feedback">
      {{ feedbackMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const userId = ref(0);
const licensePlate = ref('');
const startTime = ref('');
const endTime = ref('');
const tagId = ref(0);
const feedbackMessage = ref('');
const tags = ref([]);
const users = ref([]);
const selectedUserName = ref('');
const parkingPermissions = ref([]);
const selectedParkingPermissions = ref([]);

const openOffCanvas = () => {
  feedbackMessage.value = '';
  loadUsers();
  loadParkingPermissions();
  selectedParkingPermissions.value = [];
  UIkit.offcanvas('#offcanvas-usage').show();
};

const closeOffCanvas = () => {
  userId.value = 0;
  licensePlate.value = '';
  startTime.value = '';
  endTime.value = '';
  tagId.value = 0;
  UIkit.offcanvas('#offcanvas-usage').hide();
};

const loadUsers = async () => {
  try {
    const response = await axios.get('http://localhost:8000/users/get_users/');
    users.value = response.data;
  } catch (error) {
    console.error('Error loading users:', error);
  }
};

const selectUser = (user) => {
  userId.value = user.UserID;
  selectedUserName.value = user.userName;
};

// Function to load tags
const loadTags = async () => {
  try {
    const response = await axios.get('http://localhost:8000/tags/get_tags/');
    tags.value = response.data;
  } catch (error) {
    console.error('Error loading tags:', error);
  }
};

// Function to load parking permissions
const loadParkingPermissions = async () => {
  try {
    const response = await axios.get('http://localhost:8000/parking_permissions/get_parking_permissions/');
    parkingPermissions.value = response.data;
  } catch (error) {
    console.error('Error loading parking permissions:', error);
  }
};

const updateSelectedPermissions = (permissionType) => {
  console.log('Before update:', selectedParkingPermissions.value);

  if (selectedParkingPermissions.value.includes(permissionType)) {
    selectedParkingPermissions.value.splice(selectedParkingPermissions.value.indexOf(permissionType), 1);
  } else {
    selectedParkingPermissions.value.push(permissionType);
  }

  console.log('After update:', selectedParkingPermissions.value);
};

const postVehicle = async () => {
  try {
    console.log(selectedParkingPermissions.value);
    const response = await axios.post('http://localhost:8000/vehicles/post_vehicle/', {
      UsersID: userId.value,
      LicensePlate: licensePlate.value,
      StartTime: startTime.value,
      EndTime: endTime.value,
      TagID: tagId.value,
      PermissionID: selectedParkingPermissions.value,
    });

    // Handle the response as needed (e.g., show a success message, update UI, etc.)
    console.log('Vehicle created:', response.data);
    feedbackMessage.value = 'Vehicle created successfully';

    
    closeOffCanvas();

   
    
  } catch (error) {
    console.error('Error creating vehicle:', error);
    feedbackMessage.value = 'Error creating vehicle';
  }
  window.location.reload(); 
};

// Call loadTags and loadParkingPermissions on component mount
onMounted(async () => {
  loadTags();
  loadParkingPermissions();
  loadUsers();
});
</script>


<style scoped>
  .feedback {
    margin-top: 10px;
    color: #ff0000;
  }

  .uk-button-primary {
    background-color: #45a049;
  }

  .uk-button-primary:hover {
    background-color: #00506b;
  }

  .uk-button-small {
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .uk-input {
    margin-top: 5px;
  }
</style>
