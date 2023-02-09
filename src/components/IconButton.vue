<template>
  <button class="button">
    <i :class="`${icon} right padding`"></i>
  </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    icon: String,
  },
  setup() {
    
  },
})
</script>

<style scoped>
.padding {
  padding: 0.5rem;
}

.button:hover {
  background-color: var(--foreground);
}
</style>
