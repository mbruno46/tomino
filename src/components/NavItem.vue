<template>
  <div class="nav-item">
    <i :class="icon"></i>
    <span>
      <slot></slot>
    </span>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
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

.nav-item i {
  vertical-align: middle;
  padding: 0.2rem;
}

.nav-item:hover {
  background-color: var(--background-light);
}
</style>