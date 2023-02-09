<template>
  <div class="tab" :class="open ? 'open' : ''">
    <nav-label @click="focus(name)" :name="name"></nav-label>
    <iconify class="close" @click="close(name)" :tag="'close'"></iconify>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Iconify from './Iconify.vue';
import NavLabel from './NavLabel.vue';
import store from '@/helpers/Store'

export default defineComponent({
  components: { Iconify, NavLabel },
  props: {
    name: {
      type: String,
      default: ''
    },
    open: {
      type: Boolean,
      default: false,
    }
  },
  methods: {
    close(name: string|undefined) {
      if (name) store.Editor.closeFile(name);
    },
    focus(name: string|undefined) {
      if (name) store.Editor.focusFile(name);
    },
  },
  setup() {
  },
})
</script>

<style scoped>
.tab {
  height: min-content;
  padding: 0.5rem;
  display: grid;
  grid-template-columns: min-content min-content;
}

.tab:hover {
  cursor: pointer;
}

.tab.open {
  background: var(--background-light);
  color: var(--text);
}

.tab .close:hover {
  background-color: var(--selection-dark);
  border-radius: 4px;
}
</style>