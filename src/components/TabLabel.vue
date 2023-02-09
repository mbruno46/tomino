<template>
  <div class="tab" :class="open ? 'open' : ''">
    <span @click="focus(name)" class="padding">{{ name }}</span>
    <i class="ri-close-line padding" @click="close(name)"></i>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import store from '@/helpers/Store'

export default defineComponent({
  props: {
    name: String,
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
  width: fit-content;
  /* margin: 0.5rem; */
  padding: 0.5rem;
}
.tab:hover {
  cursor: pointer;
}

.tab.open {
  background: var(--background-light);
  color: var(--text);
}

.tab i {
  vertical-align: middle;
}

.tab i:hover {
  background: var(--selection);
}

.padding {
  padding: 0.5rem;
}
</style>