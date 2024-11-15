<script setup lang="ts">
  import { ref, computed, onBeforeMount } from 'vue';
  import VueCookie from 'vue-cookie';
  import { useRouter } from 'vue-router';
  import { request } from '@/utils/globalFunctions';
  import Task from './TaskComponent.vue'
  import { useToast } from 'vue-toastification';

  function parse_timestamp(dateString:string){ // Example date string
    const [datePart, timePart] = dateString.split(" ");  // Split into date and time

    const [month, day, year] = datePart.split("/");  // Split date part into month, day, and year
    const [hours, minutes, seconds] = timePart.split(":");  // Split time part into hours, minutes, and seconds

    // Fix two-digit year by assuming it's 2000s
    const fullYear = `20${year}`;

    // Create a new Date object using the parsed values
    const timestamp = new Date(`${fullYear}-${month}-${day}T${hours}:${minutes}:${seconds}`).getTime();

    return timestamp;
  }

  const create_task_form = ref(false);
  const router = useRouter();
  const toast = useToast();
  const show_done = ref(false);
  const full_task_list = ref<unknown[]>([]);
  const task_list = computed(
    () => full_task_list.value.filter((task: any) => task.done === false || show_done.value)
    .sort((a: any, b: any) => {
      // First, compare by done status (false first)
      if (a.done === b.done) {
        // If the done status is the same, then sort by created_at (descending)
        const sort_direction = (parse_timestamp(b.created_at) - parse_timestamp(a.created_at));
        return new_first.value ? sort_direction : sort_direction * -1;
      }
      // Tasks with done === false come first
      const doneOrder = done_first.value ? -1 : 1;
      return a.done ? doneOrder : -doneOrder;
    })
  );
  const title = ref('');
  const desc = ref('');
  const done_first = ref(false);
  const new_first = ref(true);
  onBeforeMount(async () => {
      // Check if token exists in cookies
      if (!VueCookie.get("token")) {
        router.replace('/signinform');
      } else {
        const response = await request('/tasks/', 'GET', { user_id: VueCookie.get('id') }, VueCookie.get('token'));

        // Check if the response status is 401 (Unauthorized)
        if (response.status === 401) {
          VueCookie.delete("id");
          VueCookie.delete("token");
          router.replace('/signinform');
        }
        if (response.body.tasks){
          full_task_list.value = response.body.tasks;
        }
      }
    });
  async function show_hide_done(){
    show_done.value = !show_done.value;
  }
  async function create_task(){
    const response = await request('/tasks/create_task', 'POST', { user_id: VueCookie.get('id'), title: title.value,description: desc.value,}, VueCookie.get('token'));

    if (response.body.result){
      const new_task = response.body;
      full_task_list.value.push({
        'id': new_task.id,
        'title': new_task.title,
        'description': new_task.description,
        'created_at': new_task.created_at,
        'done': false,
      })
      create_task_form.value = false;
    }
    else{
      toast.error(response.body.message)
    }
  }
  async function update_task_done(id:number, done_value:boolean) {
    const response = await request('/tasks/update', 'PUT', { user_id: VueCookie.get('id'), task_id: id, done: done_value }, VueCookie.get('token'));
    if (response.body.tasks) {
      full_task_list.value = response.body.tasks
      toast.success('Task updated')
    }
  }
  async function delete_task(id:number) {
    const response = await request('/tasks/delete', 'DELETE', { user_id: VueCookie.get('id'), task_id: id}, VueCookie.get('token'));
    if (response.body.tasks) {
      full_task_list.value = response.body.tasks
      toast.success('Task deleted')
    }
  }
  async function edit_task(id:number, title:string, desc:string) {
    const response = await request('/tasks/update', 'POST', { user_id: VueCookie.get('id'), task_id: id, title: title.value, description: desc.value}, VueCookie.get('token'));
    if (response.body.tasks) {
      full_task_list.value = response.body.tasks
      toast.success('Task updated successfully')
    }
  }
  async function logout() {
    VueCookie.delete("id");
    VueCookie.delete("token");
    router.push('/signinform');
  }
</script>

<template>
  <div class="logout">
    <a class="logout-button" @click="logout">Log out</a>
  </div>
  <div class="create-task-form" v-if="create_task_form">
    <form @submit.prevent="create_task">
      <div class="form-group title-group">
        <h2 class="form-title">Create task</h2>
        <div class="close-btn" @click="create_task_form=false">
          <span class="bar1" />
          <span class="bar2" />
        </div>
      </div>
      <div class="form-group">
        <label for="title">Title</label>
        <input type="text" v-model="title" id="title" required />
      </div>
      <div class="form-group">
        <label for="desc">Description</label>
        <input type="textarea" v-model="desc" id="desc" required />
      </div>
      <button type="submit" class="submit-btn">Create</button>
    </form>
  </div>
  <div class="task-container">
    <div class='header' >
      <div class="title">
        <h1>
          Task list
        </h1>
      </div>
      <div class="actions">
        <div class="show-completed-btn">
          <a @click="show_hide_done">{{ show_done ? 'Hide' : 'Show' }} completed</a>
        </div>
        <div class="add-task-btn">
          <i class="fas fa-plus" />
          <a @click="create_task_form=true">Add task</a>
        </div>
      </div>
    </div>
    <div class="tasks" >
      <div class="filters">
        <div class="status" @click="done_first=!done_first">
          <a>{{ done_first ? 'Done first' : 'Done last' }}</a>
        </div>
        <div class="created-at" @click="new_first=!new_first">
          <a>{{ new_first ? 'New first' : 'Old first' }}</a>
        </div>
      </div>
      <div  class="task-list">
        <Task
        @task_done="update_task_done"
        @delete_task="delete_task"
        @edit_task="edit_task"
          v-for="task_data in task_list"
          :key="Number(task_data.id)"
          :id="Number(task_data.id)"
          :title="task_data.title"
          :description="task_data.description"
          :created_at="task_data.created_at"
          :task_done="task_data.done"
        />
      </div>
    </div>
  </div>
</template>

<style lang="less" scoped>
  a{
    cursor: pointer;
  }
  .logout{
    position: absolute;
    right: 2vw;
    top: 1vh;
    & > a{
      background-color: #777;
      border-radius: 5px;
      padding: 5px 10px;
      border-radius: 5px;
      color: #fff;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      &:hover{
        background-color: #555;
      }
    }
  }
  .create-task-form{
    position: absolute;
    z-index: 99;
    left:0;
    top:0;
    display: flex;
    width: 100vw;
    height: 100vh;
    justify-content: center;
    align-items: center;
    background-color: rgba(#777, 0.3);
    & .title-group{
      position: relative;
      & > .close-btn{
        position: absolute;
        right: -5px;
        top: -5px;
        height: 25px;
        width: 25px;
        border-radius: 25px;
        background-color: rgba(#777, 0.3);
        & > .bar1, .bar2{
          position: absolute;
          left: ~"calc(50% - 1.5px)";
          top: 2px;
          display: block;
          width: 3px;
          height: 20px;
          border-radius: 5px;
          background-color: #fff;
        }
        & > .bar1{
          transform: rotate(45deg);
        }
        & > .bar2{
          transform: rotate(-45deg);
        }
      }
    }
    & > form{
      display: flex;
      height: fit-content;
      flex-direction: column;
      background-color: #fff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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

  .form-title {
    text-align: center;
    color: #555;
  }
  }
  .task-container{
    margin: auto;
    padding: 20px;
    padding-bottom: 0;
    margin-top: 15vh;
    color: #1f1f1f;
    display: flex;
    width: 40vw;
    height: 85vh;
    flex-direction: column;
    border: 1px solid black;
    border-bottom: 0;
    border-radius: 10px 10px 0 0;
    & > div.header{
      height: 10%;
      min-height: 50px;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
      & .actions {
        display: flex;
        flex-direction: row;
        & > div{
          display: flex;
          align-items: center;
          color: #1f1f1f;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
          border-radius: 10px;
          padding: 0 10px;
          &:hover{
            background-color: #ddd;
          }
          &.add-task-btn{
            margin-left: 5px;
          }
          & a{
            color: #1f1f1f;
            &:hover{
              background-color: unset;
            }
          }
        }
      }

    }
    & > div.tasks{
      height: 100%;
      padding: 10px;
      border-radius: 10px 10px 0 0;
      box-shadow: 0px 4px 8px 0px rgba(34, 60, 80, 0.2) inset;
      & > div.filters{
        overflow-y: scroll;
        position: relative;
        display: flex;
        flex-direction: row;
        width: 100%;
        min-height: 50px;
        box-shadow: 0px 4px 8px 0px rgba(34, 60, 80, 0.2);
        margin-bottom: 15px;
        border-radius: 10px;
        padding: 5px;
        & > div{
          display: flex;
          flex-direction: row;
          align-items: center;
          width: 100%;
          & > a{
            display: block;
            color: #1f1f1f;
            background-color: transparent;
            border: none;
            outline: none;
          }
        }
        & > .status{
          width: 50%;
        }
        & > .created-at{
          justify-content: flex-end;
          width: 50%;
        }
      }
    }
  }

  @media screen and (max-width: 1240px) {
    .task-container{
      width: 80vw;
      height: 85vh;
    }
  }
  @media screen and (max-width: 1024px) {
    .task-container{
      & > .header{
        height: 15% !important;
        .title{
          font-size: smaller;
        }
      }
      margin-top: 5vh;
      width: 100%;
      height: 95vh;
      border: 0;
    }
  }
</style>
