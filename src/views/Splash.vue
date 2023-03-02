<template>
  <div class="splash" :class="(hide)? 'hide': ''">
    <img src="@/assets/512x512.png">    
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';

const hide = ref(false);
onMounted(()=>{
  hide.value = true;
})
</script>

<style scoped>
.splash {
  height: 100%;
  width: 100%;
  position: fixed;
  text-align: center;
  left: 0;
  top: 0;
}

.hide {
  visibility: hidden;
  opacity: 0;
  transition: opacity 1s, visibility 1s;
}

.splash img {
  position: relative;
  height: 100%;
}
</style>