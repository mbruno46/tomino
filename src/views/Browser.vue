<template>
  <div class="browser">
    <div class="upperbar">
      <div class="title">PROJECT</div>
      <div class="buttons right">
        <!-- <icon-button :tag="'reload'" @click="reload"></icon-button> -->
        <icon-button :tag="'add-file'" @click="newFile"></icon-button>
        <icon-button :tag="'add-folder'" @click="newFolder"></icon-button>
      </div>
    </div>
    <input-field ref="inputfield"></input-field>
    <div class="filebrowser">
      <navigation-folder v-if="folder" :path="folder"></navigation-folder>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watchEffect } from 'vue'
import { exists, writeFile, createDir } from '@tauri-apps/api/fs';
import { open, save, message } from '@tauri-apps/api/dialog';

import NavigationFolder from '@/components/NavigationFolder.vue';
import IconButton from '@/components/IconButton.vue';
import InputField from '@/components/InputField.vue';

import store from '@/helpers/Store';
import { initLatexDB, fs } from '@/helpers/LatexDB';
import { wrapper } from '@/helpers/Utils';
import { CreateProject } from '@/helpers/Utils';

const folder = ref('');

wrapper('newproject', ()=>{
  save().then((path) => {
    if (path) exists(path).then((yes) => {
      if (!yes) {
        CreateProject(path).then((out)=>{
          if (out) folder.value = path;
          else message(`Error: folder ${path} could not be created`);
        })
      }
    })
  });
});

wrapper('openfolder', ()=>{
  open({directory: true, multiple: false, recursive: true}).then((dir) => {
    if ((dir!=null) && !Array.isArray(dir)) {
      fs.init(dir);
      folder.value = dir;
    }
  });
});

wrapper('setmain', ()=>{
  let fname = store.Editor.currentFile();
  initLatexDB(`${folder.value}/${fname}`)
});

export default defineComponent({
  components: {
    NavigationFolder, IconButton, InputField,
  },
  setup() {
    const inputfield = ref<typeof InputField|null>(null);

    function newFile() {
      function inner(fname: string) {
        let path = `${folder.value}/${fname}`;
        exists(path).then((yes) => {
          if (!yes) writeFile(path,'');
        })
      }
      if (folder.value!='') inputfield.value?.activate((arg:string)=>inner(arg));
    }

    function newFolder() {
      function inner(fname: string) {
        let path = `${folder.value}/${fname}`;
        exists(path).then((yes) => {
          if (!yes) createDir(path);
        })
      }
      if (folder.value!='') inputfield.value?.activate((arg:string)=>inner(arg));
    }

    onMounted(()=>{
      watchEffect(()=>{if (folder.value!='') store.pdf.value.cwd = folder.value});
      wrapper('newfile', newFile);
      wrapper('newfolder', newFolder);
    })
    // onUnmounted(()=>{unlisten();});

    return {
      folder,
      inputfield,
      newFile,
      newFolder,
    }
  },
});
</script>

<style scoped>
.browser {
  display: grid; 
  grid-template-rows: auto auto 1fr;
  height: 100%;
  overflow: hidden;
  position: relative;
}

.buttons {
  display: none;
}
.browser:hover > .upperbar .buttons{
  display: -webkit-flex;
  align-items: center;
}

.upperbar {
  width: 100%;
  height: 3rem;
  /* box-shadow: 0px 4px 6px 2px var(--background-dark); */
  box-shadow: 0px 10px 8px -8px var(--background-dark);
  display: grid;
  grid-template-columns: 1fr max-content;
}

.title {
  display: -webkit-flex;
  align-items: center;
  padding-left: 2rem;
}

.filebrowser {
  color: var(--foreground);
  overflow: scroll;
}

.right {
  float: right;
}
</style>