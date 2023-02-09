<template>
  <div class="toolbar">
    <button @click="hide_browser">
      <i :class="browser_icon"></i>
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import store from '@/helpers/Store'

export default defineComponent({
  setup() {
    const browser_icon = ref('ri-arrow-left-s-fill');

    function hide_browser() {
      store.browser.value.visible = !store.browser.value.visible;
      browser_icon.value = (store.browser.value.visible) ? 'ri-arrow-left-s-fill' : 'ri-folder-5-line';
    }

    return {
      browser_icon,
      hide_browser,
    }
  },
})
</script>

<style scoped>
.toolbar {
  width: 3rem;
  height: 100vh;
  background-color: var(--background-dark);
}

.toolbar button {
  background-color: inherit;
  color: var(--foreground);
  border: none;
  text-decoration:none;
  outline: none;
  display: inline-block;
  align-items: center;
  margin: 0rem;
  box-sizing: border-box;
  width: 3rem;
  height: 3rem;
  font-size: x-large;
}

.toolbar button:hover {
  background-color: var(--selected);
}

</style>