<template>
  <div>
    <!-- Button to open off-canvas panel -->
    <button @click="openOffCanvas" class="uk-button uk-button-primary uk-margin-small-right">
      <span uk-icon="plus"></span>
    </button>

    <!-- Off-canvas panel -->
    <div id="offcanvas-usage" uk-offcanvas="flip: true">
      <div class="uk-offcanvas-bar">

        <!-- Close button for off-canvas panel -->
        <button class="uk-offcanvas-close" type="button" @click="closeOffCanvas"></button>

        <h3>Add Vehicle</h3>

        <!-- Form for adding a new vehicle -->
        <form @submit.prevent="addVehicle">
          <div class="form-group">
            <label for="userDropdown">User:</label>
            <!-- Dropdown for selecting a user -->
            <select v-model="userId" id="userDropdown" class="uk-select" required>
              <option v-for="user in users" :key="user.userId" :value="user.userId">{{ user.userName }}</option>
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
            <!-- Dropdown for selecting a single tag -->
            <select v-model="tagId" id="tagDropdown" class="uk-select" required>
              <option v-for="tag in tags" :key="tag.tagId" :value="tag.tagId">{{ tag.tagName }}</option>
            </select>
          </div>

          <div class="form-group">
            <label for="parkingPermissions">Parking Permissions:</label>
            <!-- Multi-choice input for parking permissions -->
            <select v-model="selectedParkingPermissions" id="parkingPermissions" class="uk-select" multiple required>
              <option v-for="permission in parkingPermissions" :key="permission.permissionId" :value="permission.permissionId">
                {{ permission.permissionName }}
              </option>
            </select>
          </div>

          <button type="submit" class="uk-button uk-button-primary uk-button-small">
            <span uk-icon="plus"></span> Create & Add Vehicle
          </button>
        </form>
      </div>
    </div>

    <!-- Feedback-Element -->
    <div v-if="feedbackMessage" class="feedback">
      {{ feedbackMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const ownerName = ref('');
const licensePlate = ref('');
const tagId = ref(0);
const parkingPermissionId = ref(0);
const feedbackMessage = ref('');

const openOffCanvas = () => {
  // Reset feedback message when opening the off-canvas panel
  feedbackMessage.value = '';
  // Open the off-canvas panel
  UIkit.offcanvas('#offcanvas-usage').show();
};

const closeOffCanvas = () => {
  // Optional: Zurücksetzen der Eingabefelder
  ownerName.value = '';
  licensePlate.value = '';
  tagId.value = 0;
  parkingPermissionId.value = 0;

  // Close the off-canvas panel
  UIkit.offcanvas('#offcanvas-usage').hide();
};

const addVehicle = async () => {
  const data = {
    owner_name: ownerName.value,
    license_plate: licensePlate.value,
    tag_id: tagId.value,
    parking_permission_id: parkingPermissionId.value,
  };

  try {
    await axios.post('http://localhost:8000/vehicles/post_vehicle/', data);
    feedbackMessage.value = 'Vehicle added successfully!';

    // Wenn das Hinzufügen erfolgreich war, schließe das Off-Canvas-Panel
    closeOffCanvas();
  } catch (error) {
    console.error('Error adding vehicle:', error);
    feedbackMessage.value = 'Error adding vehicle. Please try again.';
  }
  window.location.reload();
};
</script>

<style scoped>
.feedback {
  margin-top: 10px;
  color: #ff0000; /* Rote Farbe für Fehlermeldung, optional */
}

.uk-button-primary {
  background-color: #45a049; /* Blau für Hintergrundfarbe des Primary Buttons */
}

.uk-button-primary:hover {
  background-color: #00506b; /* Dunkleres Blau beim Hover */
}

.uk-button-small {
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease; /* Smooth Hover-Effekt */
}

.uk-input {
  margin-top: 5px;
}
</style>
