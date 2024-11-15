<script lang="ts" setup>
// vue imports
import { useRouter } from 'vue-router'

// modules
const router = useRouter()

function goBack() {
  router.back()
}
</script>

<template>
  <div>
    <button type="reset" @click="goBack" class="back-btn">Back</button>
  </div>
</template>

<style lang="less" scoped>
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
</style>
