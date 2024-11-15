<script setup lang="ts">
import { ref } from 'vue';
import { request } from '@/utils/globalFunctions.ts';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';
import BackButton from '@/components/buttons/BackButton.vue';
import VueCookie from 'vue-cookie';

// Declare reactive variables
const username = ref('');
const password = ref('');

const toast = useToast();
const router = useRouter();

// Handle form submission
async function submitForm(){
  const response = await request('/users/login', 'POST', {id: 1, username: username.value, password: password.value});
  if (response.body.result){
    toast.success(response.body.message);
    VueCookie.set('token', response.body.token, { expires: '1d' });
    VueCookie.set('id', response.body.id, { expires: '1d' });
    router.replace('/tasks');
  }
  else{
    toast.error(response.body.message);
  }
};
</script>

<template>
  <div class="login-container">
    <form @submit.prevent="submitForm" class="form">
      <div class="form-group title-group">
        <BackButton />
        <h2 class="form-title">Sign in</h2>
      </div>
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit" class="submit-btn">Sign in</button>
    </form>
  </div>
</template>


<style lang="less" scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f1f1f1;
}

.form {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
}

.title-group{
  position: relative;
}

.back-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  padding: 5px 10px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
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
