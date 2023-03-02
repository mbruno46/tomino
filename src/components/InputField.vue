<template>
  <div v-if="visible" class="inputfield">
    <input ref="input" v-model="field" placeholder="filename" @mousedown="(e)=>e.stopPropagation()" @keydown="(e)=>e.stopPropagation()"/>
    <icon-button :tag="'up'" @click="ok"></icon-button>
    <icon-button :tag="'close'" @click="visible=false"></icon-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

import IconButton from './IconButton.vue';

const field = ref('');
const visible = ref(false);
const input = ref(null);
let cb: Function;

function activate(callback: Function) {
  visible.value = true;
  cb = callback;
}

function ok() {
  cb(field.value);
  visible.value = false;
}

defineExpose({ activate });
</script>

<style scoped>

.inputfield {
  width: 100%;
  display: grid;
  grid-template-columns: auto max-content max-content;
  border: 2px solid var(--background-dark);
  background-color: var(--background);
  position:sticky;
  top: 0px;
}

.inputfield input {
  padding-left: 0.5rem;
  color: var(--text);
  background-color: var(--background-light);
  font: inherit;
  width: 100%;
}
</style>