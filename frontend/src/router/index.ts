import { createRouter, createWebHistory } from 'vue-router';
import VueCookie from 'vue-cookie';

import RegisterLogin from '@/views/RegisterLogin.vue';
import RegistrationForm from '@/components/reg/RegistrationForm.vue';
import LoginForm from '@/components/reg/LoginForm.vue';
import TasksPage from '@/components/tasks/TasksPage.vue';



const routes = [
  {
    path: '/',
    redirect: () => {
      // Check if the token exists in cookies
      const token = VueCookie.get('token');
      return token ? '/tasks' : '/signinform';
    },
  },
  {
    path: '/signinform',
    name: 'signinform',
    component: RegisterLogin
  },
  {
    path: '/registration',
    name: 'registration',
    component: RegistrationForm
  },
  {
    path: '/login',
    name: 'login',
    component: LoginForm
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: TasksPage
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
