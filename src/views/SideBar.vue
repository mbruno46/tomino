<template>
  <div class="toolbar">
    <button @click="hide_browser">
      <iconify class='icons' :tag="browser_icon"></iconify>
    </button>
    <button>
      <iconify class='icons' :tag="'refresh'"></iconify>
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import store from '@/helpers/Store'
import Iconify from '@/components/Iconify.vue';

export default defineComponent({
  components: {
    Iconify,
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
}

.icons {
  vertical-align: top;
  font-size: 1.6rem;
}

.toolbar button:hover {
  background-color: var(--selected);
}

</style>