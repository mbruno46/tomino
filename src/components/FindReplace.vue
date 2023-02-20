<template>
  <div class="findreplace" contenteditable="false">
    <input placeholder="find" @mousedown="(e)=>e.stopPropagation()" @keydown="(e)=>e.stopPropagation()"/>
    <icon-button :tag="'down'"></icon-button>
    <icon-button :tag="'up'"></icon-button>
    <!-- <input placeholder="replace"/> -->
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import IconButton from './IconButton.vue';

export default defineComponent({
  components: {
    IconButton,
  },
  setup() {
  }
});
</script>

<style scoped>
.findreplace {
  display: grid;
  grid-template-rows: min-content min-content;
  grid-template-columns: minmax(30%, 1fr) min-content min-content;
  border: 2px solid var(--background-dark);
  background-color: var(--background);
}

.findreplace input {
  padding: 0.5rem;
  color: var(--text);
  background-color: var(--background-light);
  font: inherit;
}
</style>