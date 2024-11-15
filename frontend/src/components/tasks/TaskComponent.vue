<script lang="ts" setup>
// vue imports
import { ref, computed, defineProps, defineEmits } from 'vue'

const emit = defineEmits(['task_done', 'delete_task', 'edit_task'])

// props
const task_data = defineProps({
  id: {
    type: Number,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  created_at: {
    type: String,
    required: true,
  },
  task_done: {
    type: Boolean,
    required: false,
    default: false,
  },
})

const edit_title = ref(task_data.title)
const edit_desc = ref(task_data.description)
const edit_task_form = ref(false)

const is_task_done = computed(() => (task_data.task_done ? 'done' : null))

async function edit_task() {
  emit('edit_task', task_data.id, edit_title, edit_desc)
  edit_task_form.value = false
}
</script>

<template>
  <div class="edit-task-form" v-if="edit_task_form">
    <form @submit.prevent="edit_task">
      <div class="form-group title-group">
        <h2 class="form-title">Edit task</h2>
        <div class="close-btn" @click="edit_task_form = false">
          <span class="bar1" />
          <span class="bar2" />
        </div>
      </div>
      <div class="form-group">
        <label for="title">Title</label>
        <input type="text" v-model="edit_title" id="title" required />
      </div>
      <div class="form-group">
        <label for="desc">Description</label>
        <input type="textarea" v-model="edit_desc" id="desc" required />
      </div>
      <button type="submit" class="submit-btn">Confirm</button>
    </form>
  </div>
  <div :class="['task', is_task_done]">
    <div class="done">
      <input
        type="checkbox"
        @click="emit('task_done', task_data.id, !task_data.task_done)"
        :checked="task_done"
      />
    </div>
    <div class="task_data">
      <h3 class="task_title">{{ task_data.title }}</h3>
      <span class="task_description"> {{ task_data.description }}</span>
      <span class="task_created_at">{{ task_data.created_at }}</span>
    </div>
    <div class="task_actions">
      <div class="edit" @click="edit_task_form = true">
        <i class="fas fa-pen-to-square" />
      </div>
      <div class="delete" @click="emit('delete_task', task_data.id)">
        <i class="fas fa-trash-can" />
      </div>
    </div>
  </div>
</template>

<style lang="less" scoped>
.edit-task-form {
  position: absolute;
  z-index: 99;
  left: 0;
  top: 0;
  display: flex;
  width: 100vw;
  height: 100vh;
  justify-content: center;
  align-items: center;
  background-color: rgba(#777, 0.3);
  & .title-group {
    position: relative;
    & > .close-btn {
      position: absolute;
      right: -5px;
      top: -5px;
      height: 25px;
      width: 25px;
      border-radius: 25px;
      background-color: rgba(#777, 0.3);
      & > .bar1,
      .bar2 {
        position: absolute;
        left: ~'calc(50% - 1.5px)';
        top: 2px;
        display: block;
        width: 3px;
        height: 20px;
        border-radius: 5px;
        background-color: #fff;
      }
      & > .bar1 {
        transform: rotate(45deg);
      }
      & > .bar2 {
        transform: rotate(-45deg);
      }
    }
  }
  & > form {
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
.task {
  position: relative;
  display: flex;
  flex-direction: row;
  width: 100%;
  min-height: 50px;
  box-shadow: 0px 4px 8px 0px rgba(34, 60, 80, 0.2);
  margin-bottom: 15px;
  border-radius: 10px;
  padding: 5px;
  .done {
    margin-left: 5px;
  }
  &.done {
    filter: opacity(0.5);
  }
  & > div {
    display: flex;
    justify-content: center;
  }
}
.task_data {
  display: flex;
  flex-grow: 1;
  margin: 0px 1rem;
  flex-direction: column;
  .task_title {
    font-weight: bold;
  }
  .task_created_at {
    color: #777;
    font-size: smaller;
  }
}
.task_actions {
  display: flex;
  align-items: center;
  div {
    width: 25px;
    height: 25px;
    color: #999;
  }
  .edit:hover {
    color: #555;
  }
  .delete:hover {
    color: #f55;
  }
}
</style>
