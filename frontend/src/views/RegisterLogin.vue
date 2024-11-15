<template>
  <div class="signupin">
    <router-link to="/login">Sing in</router-link>
    <router-link to="/registration">Sign up</router-link>
  </div>
</template>

<script setup lang="ts">
</script>

<style lang="less" scoped>
.signupin {
  text-align: center;
  display: flex;
  flex-direction: column;
  padding: 20px 30px;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  & > a {
    width: 100%;
    background-color: #d1c8b8;
    border: none;
    border-radius: 4px;
    color: #fff;
    font-size: 16px;
    cursor: pointer;
    &:hover {
      background-color: #b8ab98;
    }
    &:first-child {
      margin-bottom: 5px;
    }
  }
}
</style>
