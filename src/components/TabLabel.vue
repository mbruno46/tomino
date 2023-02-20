<template>
  <div class="tab" :class="(open ? 'open' : '') + ' ' + (modified ? 'modified' : '')">
    <nav-label @click="focus(name)" :name="name"></nav-label>
    <icon-button @click="close(name)" :tag="'close'" :fontsize="1.2"></icon-button>
  </div>
</template>
<!-- :class="open ? 'open' : ''"  -->
<script lang="ts">
import { defineComponent } from 'vue'
import NavLabel from './NavLabel.vue';
import store from '@/helpers/Store'
import IconButton from './IconButton.vue';

export default defineComponent({
  components: { IconButton, NavLabel },
  props: {
    name: {
      type: String,
      default: ''
    },
    open: {
      type: Boolean,
      default: false,
    },
    modified: {
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
.modified {
  font-style: italic;
  color: var(--red) !important;
}
</style>