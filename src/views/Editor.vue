<template>
  <div class="editor">
    <div class="tabbar">
      <tab-label v-for="(val, key) in files" :key="key" 
        :open="val.open" :modified="val.modified" :name="key.toString()">
      </tab-label>
    </div>
    <code-editor v-for="(val, key) in files" :path="val.path"
      :key="`code_${key}`" :class="val.open ? '': 'hide'" :ref="(el)=>{Refs[key]=el}"
      @status="(n)=>{getStatus(key.toString(),n);}"
      @recompile="(level)=>{store.pdf.value.compile = level;}">
    </code-editor>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watchEffect } from 'vue'

import CodeEditor from '@/components/CodeEditor.vue';
import TabLabel from '@/components/TabLabel.vue';

import store from '@/helpers/Store'
import { wrapper } from '@/helpers/Utils';

import { basename } from '@tauri-apps/api/path';

function dispatch(name: string, key: Object) {
  wrapper(name, ()=>{
    let sel = store.Editor.currentFile()
    Refs.value[sel].handleKeyBoard(new KeyboardEvent('keydown', key));
  })
}
dispatch('undo', {'ctrlKey': true, 'key': 'z'});
dispatch('redo', {'ctrlKey': true, 'shiftKey': true, 'key': 'z'});
dispatch('cut', {'ctrlKey': true, 'key': 'x'});
dispatch('copy', {'ctrlKey': true, 'key': 'c'});
dispatch('paste', {'ctrlKey': true, 'key': 'v'});
dispatch('find', {'ctrlKey': true, 'key': 'f'});
dispatch('save', {'ctrlKey': true, 'key': 's'});

const files = computed(() => store.Editor.files);
const Refs = ref<{[key:string]: any}>({});

onMounted(()=>{
  watchEffect(()=>{
    let s = store.pdf.value.synctex;
    if (s.sync) {
      basename(s.path).then((name) => {
        store.Editor.openFile(s.path, name);
        if (name in Refs.value) Refs.value[name].setSelection(s.line-1, s.column);
      });
      s.sync = false;
    }
  })
});

function getStatus(name: string, status: number) {
  if (status==1) {files.value[name].modified = true}
  else if (status==2) {files.value[name].modified = false}
}

</script>


<style scoped>
.editor {
  height: 100%;
  overflow: hidden;
  background: var(--background-light);
  position: relative;
}

.tabbar {
  display: flex;
  flex-direction: row;
  width: 100%;
  overflow-y: hidden;
  overflow-x: scroll;
  background: var(--background-dark);
}

.tabbar::-webkit-scrollbar {
  display: none;
}

.hide {
  visibility: hidden;
  opacity: 0;
}

</style>