<template>
  <div class="registration-container">
    <h2>Registration</h2>
    <form @submit.prevent="register" class="registration-form">
      <div class="form-group">
        <label for="username">Username:</label>
        <input v-model="username" type="text" id="username" required />
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input v-model="email" type="email" id="email" required />
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" required />
      </div>

      <div class="form-group">
        <label for="phonenumber">Phone Number:</label>
        <input v-model="phonenumber" type="text" id="phonenumber" />
      </div>

      <button type="submit" class="register-button">Register</button>
    </form>
    <router-link to="/login" class="login-link">Already have an account? Back to Login here.</router-link>
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
        const crypto = require('crypto');
        return crypto.randomBytes(length).toString('hex');
      } else {
        const randomBytesArray = new Uint8Array(length);
        window.crypto.getRandomValues(randomBytesArray);
        return Array.from(randomBytesArray)
          .map((byte) => byte.toString(16).padStart(2, '0'))
          .join('');
      }
    },

    async register() {
      try {
        const salt = this.generateRandomString(16);
        const registrationData = {
          Username: this.username,
          Email: this.email,
          Password: this.password,
          PhoneNumber: this.phonenumber,
          Salt: salt,  
        };

        console.log('Data to be sent to the API:', registrationData);
        await axios.post('http://localhost:8000/users/post_user/', registrationData);
        console.log('Registration successful!');
      } catch (error) {
        console.error('Error during registration:', error);
        this.registrationError = 'Registration failed. Please try again.';
      }
    }
  },
});
</script>

  
<style scoped>
.registration-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background: #f8f8f8;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

input {
  width: calc(100% - 16px);
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.register-button {
  width: 100%;
  padding: 10px;
  background-color: #5cb85c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.register-button:hover {
  background-color: #4cae4c;
}

.login-link {
  display: block;
  text-align: center;
  margin-top: 20px;
  color: #333;
  text-decoration: none;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #5cb85c;
}
</style>