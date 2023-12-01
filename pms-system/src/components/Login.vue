<!-- components/Login.vue -->
<template>
  <div class="login-container">
    <form @submit.prevent="login" class="login-form">
      <label for="username">Username:</label>
      <input v-model="username" type="text" id="username" required />

      <label for="password">Password:</label>
      <input v-model="password" type="password" id="password" required />

      <button type="submit" class="login-button">Login</button>
    </form>

    <router-link to="/registration" class="registration-link">
      Don't have an account? Register here.
    </router-link>
  </div>
</template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  import axios, { AxiosResponse } from 'axios';
  
  // Define the data structure for the login request
  interface LoginRequest {
    grant_type: string;
    username: string;
    password: string;
  }
  
  export default defineComponent({
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      async login() {
        try {
          // Prepare the data as per the LoginRequest structure
          const requestData: LoginRequest = {
            grant_type: 'password',
            username: this.username,
            password: this.password,
          };
  
          // Use URLSearchParams to encode the data in the required format
          const params = new URLSearchParams();
          params.append('grant_type', requestData.grant_type);
          params.append('username', requestData.username);
          params.append('password', requestData.password);
  
          const salt: AxiosResponse<{ salt: string }> = await axios.get(
            'http://localhost:8000/users/get_salt/' + this.username
          )
          // Make the login request
          const response: AxiosResponse<{ access_token: string }> = await axios.post(
            'http://localhost:8000/login',
            params.toString(), // Use the encoded form data
            {
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
              },
            }
          );
  
          // Handle successful login, e.g., store the token in local storage
          const accessToken = response.data.access_token;
          localStorage.setItem('access_token', accessToken);
  
          // Include the token in the headers for subsequent requests
          axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
  
          // Redirect to a protected route or perform any other action
          this.$router.push('/protected');
        } catch (error) {
          // Handle login error, e.g., display an error message
          console.error('Login failed:', error);
        }
      },
    },
  });
  </script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.login-form {
  width: 300px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}

.login-button {
  background-color: #45a049;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #00506b;
}

.registration-link {
  margin-top: 10px;
  color: #45a049;
  text-decoration: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.registration-link:hover {
  color: #00506b;
}
</style>