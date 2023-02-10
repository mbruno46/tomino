<template>
  <div class="toolbar">
    <icon-button :tag="browser_icon" @click="hide_browser" :fontsize="2"></icon-button>
    <icon-button :tag="'refresh'" :fontsize="2"></icon-button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import store from '@/helpers/Store'
import IconButton from '@/components/IconButton.vue';

export default defineComponent({
  components: {
    IconButton,
  },
  setup() {
    const browser_icon = ref('left-fill');

    function hide_browser() {
      store.browser.value.visible = !store.browser.value.visible;
      browser_icon.value = (store.browser.value.visible) ? 'left-fill' : 'files';
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
  display: flex;
  flex-flow: column;
  height: 100vh;
  background-color: var(--background-dark);
}

/* .toolbar button {
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
}
.toolbar button:hover {
  background-color: var(--selected);
} */

</style>