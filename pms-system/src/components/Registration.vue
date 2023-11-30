<!-- Registration.vue -->
<template>
    <div>
      <h2>Registration</h2>
      <form @submit.prevent="register">
        <label for="username">Username:</label>
        <input v-model="username" type="text" id="username" required />
  
        <label for="email">Email:</label>
        <input v-model="email" type="email" id="email" required />
  
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" required />
  
        <label for="phonenumber">Phone Number:</label>
        <input v-model="phonenumber" type="text" id="phonenumber" />
  
        <button type="button" @click="register">Register</button>
      </form>
      <router-link to="/login">Already have an account? Back to Login here.</router-link>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import axios from 'axios';
  
  export default defineComponent({
    data() {
      return {
        username: '',
        email: '',
        password: '',
        phonenumber: '',
        registrationError: null as string | null,
      };
    },
    methods: {
        generateRandomString(length: number): string {
            if (typeof window === 'undefined') {
                // We are in a Node.js environment
                const crypto = require('crypto');
                return crypto.randomBytes(length).toString('hex');
            } else {
                // We are in a browser environment
                const randomBytesArray = new Uint8Array(length);
                window.crypto.getRandomValues(randomBytesArray);
                return Array.from(randomBytesArray)
                .map((byte) => byte.toString(16).padStart(2, '0'))
                .join('');
            }
        },

        async register() {
    try {
        // Generiere ein zufälliges Salt
        const salt = this.generateRandomString(16);

        // Verwende die hashPassword-Funktion im Frontend, um das Passwort zu hashen
       // const hashedPassword = this.generateRandomString(16);

        const registrationData = {
            Username: this.username,
            Email: this.email,
            Password: this.password,
            PhoneNumber: this.phonenumber,
            Salt: salt,  // Füge das generierte Salt hinzu
        };

        // Protokolliere die Daten, die an die API gesendet werden
        console.log('Data to be sent to the API:', registrationData);

        // Beachte, dass wir hier nicht auf die Antwort warten können
        await axios.post('http://localhost:8000/users/post_user/', registrationData);

        // Handle successful registration
        console.log('Registration successful!');
    } catch (error) {
        console.error('Error during registration:', error);

        // Handle registration error
        this.registrationError = 'Registration failed. Please try again.';
    }
}

    },
  });
  </script>
  
  <style scoped>
  /* Style to display labels and inputs vertically */
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
  }
  </style>
  