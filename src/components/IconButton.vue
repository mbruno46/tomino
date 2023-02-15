<template>
  <button class="icon-button"> 
    <iconify :tag="tag" :style="`font-size: ${fontsize}rem;`"></iconify>
  </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Iconify from './Iconify.vue';

export default defineComponent({
  components: {
    Iconify,
  },
  props: {
    tag: String,
    fontsize: {
      type: Number,
      default: 1.6,
    }
  },
  setup() {
  }
});
</script>

<style scoped>
.icon-button {
  background-color: inherit;
  color: var(--foreground);
  border: none;
  text-decoration:none;
  outline: none;
  display: -webkit-inline-flex;
  align-items: center;
  margin: 0rem;
  padding: 0.5rem;
  box-sizing: border-box;
  width: min-content;
  aspect-ratio: 1;
  /* height: 3rem; */
}

.icon-button:hover {
  background-color: var(--selection-dark);
  color: var(--text);
  border-radius: 16px;
}

</style>