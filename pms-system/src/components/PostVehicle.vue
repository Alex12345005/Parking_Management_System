<template>
    <div>
      <button @click="openPopup" class="add-vehicle-button">Fahrzeug hinzufügen</button>
      <div v-if="isPopupVisible" class="popup">
        <form @submit.prevent="addVehicle">
          <div class="form-group">
            <label for="ownerName">Besitzername:</label>
            <input v-model="ownerName" type="text" id="ownerName" required />
          </div>
  
          <div class="form-group">
            <label for="licensePlate">Kennzeichen:</label>
            <input v-model="licensePlate" type="text" id="licensePlate" required />
          </div>
  
          <div class="form-group">
            <label for="tagId">Tag ID:</label>
            <input v-model="tagId" type="number" id="tagId" required />
          </div>
  
          <div class="form-group">
            <label for="parkingPermissionId">Parkberechtigung ID:</label>
            <input v-model="parkingPermissionId" type="number" id="parkingPermissionId" required />
          </div>
  
          <button type="submit" class="post-button">Fahrzeug hinzufügen</button>
        </form>
  
        <!-- Feedback-Element -->
        <div v-if="feedbackMessage" class="feedback">
          {{ feedbackMessage }}
        </div>
      </div>
  
      <!-- Hintergrund-Overlay mit Blur-Effekt -->
      <div v-if="isPopupVisible" class="background-overlay"></div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  
  const isPopupVisible = ref(false);
  const ownerName = ref('');
  const licensePlate = ref('');
  const tagId = ref(0);
  const parkingPermissionId = ref(0);
  const feedbackMessage = ref('');
  
  const openPopup = () => {
    isPopupVisible.value = true;
    feedbackMessage.value = ''; // Reset feedback message when opening the popup
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
      feedbackMessage.value = 'Fahrzeug erfolgreich hinzugefügt!';
  
      // Wenn das Hinzufügen erfolgreich war, setze das Popup zurück
      isPopupVisible.value = false;
      ownerName.value = '';
      licensePlate.value = '';
      tagId.value = 0;
      parkingPermissionId.value = 0;
    } catch (error) {
      console.error('Fehler beim Hinzufügen des Fahrzeugs:', error);
      feedbackMessage.value = 'Fehler beim Hinzufügen des Fahrzeugs. Bitte versuche es erneut.';
    }
  };
  </script>
  
  <style scoped>

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border: 1px solid #ccc;
  color: black;
  z-index: 1000;
}

.background-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3); /* Schwarzes Overlay mit Transparenz für den Blur-Effekt */
  backdrop-filter: blur(5px); /* Blur-Effekt */
  z-index: 999; /* Darunterliegendes Popup überlagern */
}
  .feedback {
    margin-top: 10px;
    color: #ff0000; /* Rote Farbe für Fehlermeldung, optional */
  }
  
  .add-vehicle-button {
    background-color: #4caf50; /* Grün für Hintergrundfarbe */
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease; /* Smooth Hover-Effekt */
    margin-top: 15px;
  }
  
  .add-vehicle-button:hover {
    background-color: #45a049; /* Dunkleres Grün beim Hover */
  }
  
  .post-button {
    background-color: #45a049; /* Blau für Hintergrundfarbe des Post-Buttons */
    color: white;
    padding: 5px 10px;
    border: none;
    margin-top: 5px;
    margin-left: 5px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease; /* Smooth Hover-Effekt */
  }
  
  .post-button:hover {
    background-color: #00506b; /* Dunkleres Blau beim Hover */
  }
  </style>
  