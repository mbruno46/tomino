<template>
  <div class="nav-item">
    <span>
      <iconify :icon="icon"></iconify>
    </span>
    <span>
      <slot></slot>
    </span>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Iconify from './Iconify.vue';

export default defineComponent({
  components: { Iconify },
  props: {
    icon: String,
  },
  // setup() {
  // },
})
</script>

<style scoped>
.nav-item {
  padding-top: 0.2rem;
  padding-bottom: 0.2rem;
}

.nav-item span {
  vertical-align: top;
  padding: 0.2rem;
}

.nav-item:hover {
  background-color: var(--background-light);
}
</style>