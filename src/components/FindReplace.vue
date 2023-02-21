<template>
  <div v-if="visible" class="findreplace" contenteditable="false">
    <input v-model="find" placeholder="find" @mousedown="(e)=>e.stopPropagation()" @keydown="(e)=>e.stopPropagation()"/>
    <icon-button :tag="'down'" @click="$emit('findword',find,true)"></icon-button>
    <icon-button :tag="'up'" @click="$emit('findword',find,false)"></icon-button>
    <input v-model="replace" placeholder="replace" @mousedown="(e)=>e.stopPropagation()" @keydown="(e)=>e.stopPropagation()"/>
    <icon-button :tag="'replace'" @click="$emit('replace',find,replace)"></icon-button>
    <icon-button :tag="'close'" @click="visible=false"></icon-button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

import IconButton from './IconButton.vue';

export default defineComponent({
  components: {
    IconButton,
  },
  emits: ['findword','replace'],
  setup() {
    const visible = ref(false);
    const find = ref('');
    const replace = ref('');
    return {
      visible,
      find,
      replace,
    }
  },
  methods: {
    activate() {
      this.visible = true;
    },
  }
});
</script>

<style scoped>
.findreplace {
  display: grid;
  grid-template-rows: max-content max-content;
  grid-template-columns: minmax(30%, 1fr) max-content max-content;
  border: 2px solid var(--background-dark);
  background-color: var(--background);
  position:sticky;
  bottom: 0px;
}

.findreplace input {
  padding-left: 0.5rem;
  color: var(--text);
  background-color: var(--background-light);
  font: inherit;
}
</style>