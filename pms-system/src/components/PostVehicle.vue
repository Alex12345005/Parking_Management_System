<template>
  <div>
    <button @click="openOffCanvas" class="uk-button uk-button-secondary uk-margin-right uk-button-small"><a href="" uk-icon="plus"></a>Vehicle</button>
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

          <!-- Dropdown for selecting a single tag -->
          <div class="form-group">
            <label for="tagDropdown">Tag:</label>
            <select v-model="tagId" id="tagDropdown" class="uk-select" required>
              <option v-for="tag in tags" :key="tag.tagId" :value="tag.tagId">{{ tag.tagName }}</option>
            </select>
          </div>

          <div class="form-group">
            <label for="parkingPermissions">Parking Permissions:</label>
            <!-- Multi-choice input for parking permissions -->
            <select v-model="selectedParkingPermissions" id="parkingPermissions" class="uk-select" multiple required>
            </select>
          </div>

          <button type="submit" class="uk-button uk-button-primary uk-button-small">
            <span uk-icon="plus"></span> Create new Vehicle
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
import { ref, onMounted } from 'vue';
import axios from 'axios';

const userId = ref(0);
const licensePlate = ref('');
const startTime = ref('');
const endTime = ref('');
const tagId = ref(0);
const selectedParkingPermissions = ref([]);
const feedbackMessage = ref('');
const tags = ref([]);
const users = ref([]);  // You need to provide the users data

const openOffCanvas = () => {
  // Reset feedback message when opening the off-canvas panel
  feedbackMessage.value = '';
  // Open the off-canvas panel
  UIkit.offcanvas('#offcanvas-usage').show();
};

const closeOffCanvas = () => {
  // Optional: Zurücksetzen der Eingabefelder
  userId.value = 0;
  licensePlate.value = '';
  startTime.value = '';
  endTime.value = '';
  tagId.value = 0;
  selectedParkingPermissions.value = [];

  // Close the off-canvas panel
  UIkit.offcanvas('#offcanvas-usage').hide();
};

// Funktion zum Laden der Tags
const loadTags = async () => {
  try {
    const response = await axios.get('http://localhost:8000/tags/get_tags_name/');
    console.log('Tags data:', response.data);
    tags.value = response.data;
  } catch (error) {
    console.error('Error loading tags:', error);
  }
};

// Beim Laden der Komponente die Tags laden
onMounted(() => {
  loadTags();
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

  #tagDropdown {
    color: black;
  }

  #offcanvas-usage #tagDropdown {
    color: black;
  }
</style>
