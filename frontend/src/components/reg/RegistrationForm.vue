<script setup lang="ts">
// node modules
import { ref } from 'vue'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'
import VueCookie from 'vue-cookie'

// components
import BackButton from '@/components/buttons/BackButton.vue'

// functions
import { request } from '@/utils/globalFunctions'

// modules
const toast = useToast()
const router = useRouter()

// Declare reactive variables
const username = ref('')
const password = ref('')
const confirmPassword = ref('')

// Handle form submission
async function submitForm() {
  const response = await request('/users/add_user', 'POST', {
    username: username.value,
    password: password.value,
  })
  if (response.body.result) {
    toast.success(response.body.message)
    VueCookie.set('auth', true);
    router.replace('/tasks')
  } else {
    toast.error(response.body.message)
  }
}
</script>

<template>
  <div class="registration-container">
    <form @submit.prevent="submitForm" class="form">
      <div class="form-group title-group">
        <BackButton />
        <h2 class="form-title">Sign up</h2>
      </div>
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input
          :class="{
            error: password && confirmPassword && password !== confirmPassword,
          }"
          type="password"
          id="password"
          v-model="password"
          required
        />
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input
          :class="{
            error: password && confirmPassword && password !== confirmPassword,
          }"
          type="password"
          id="confirmPassword"
          v-model="confirmPassword"
          required
        />
        <div class="error_div">
          <p v-if="password && confirmPassword && password !== confirmPassword" class="error">
            Passwords do not match.
          </p>
        </div>
      </div>
      <button type="submit" class="submit-btn" :disabled="password !== confirmPassword">
        Register
      </button>
    </form>
  </div>
</template>

<style scoped>
.registration-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f1f1f1;
}

input.error {
  box-shadow: 0 0 8px rgba(255, 0, 0, 0.5);
}

div.error_div {
  min-height: 25px;
}

p.error {
  color: red;
  font-size: 0.9em;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:disabled:hover {
  background-color: #ccc;
}

.form {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
}

.title-group {
  position: relative;
}

.form-title {
  text-align: center;
  color: #555;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
  color: #777;
}

input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.submit-btn {
  width: 100%;
  padding: 10px;
  background-color: #d1c8b8;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #b8ab98;
}
</style>
