<template>
  <div class="browser">
    <div class="upperbar">
      <div class="title">PROJECT</div>
      <div class="buttons right">
        <icon-button :tag="'reload'" @click="reload"></icon-button>
        <icon-button :tag="'add-file'" @click="newFile"></icon-button>
        <icon-button :tag="'add-folder'" @click="newFolder"></icon-button>
      </div>
    </div>
    <input-field ref="inputfield"></input-field>
    <div class="filebrowser">
      <nav-folder v-if="filetree" :ftree="filetree"></nav-folder>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watchEffect } from 'vue'
import { readDir, exists, writeFile, createDir } from '@tauri-apps/api/fs';
import { open, save } from '@tauri-apps/api/dialog';

import NavFolder from '@/components/NavFolder.vue';
import IconButton from '@/components/IconButton.vue';
import InputField from '@/components/InputField.vue';

import { FileTree } from '@/helpers/FileTree';
import store from '@/helpers/Store';
import database from '@/helpers/LatexData';
import { wrapper } from '@/helpers/Utils';
import { FileWatcher } from '@/helpers/Utils';

const folder = ref('');

wrapper('newproject', ()=>{
  save({title: 'Create new project'}).then((path) => {
    if (path) {
      exists(path).then((yes)=>{
        if (!yes) createDir(path).then(()=>folder.value = path);
        else folder.value
      })
    }
  });
});

wrapper('openfolder', ()=>{
  open({directory: true, multiple: false, recursive: true}).then((dir) => {
    if ((dir!=null) && !Array.isArray(dir)) {
      folder.value = dir;
    }
  });
});

wrapper('setmain', ()=>{
  let fname = store.Editor.currentFile();
  exists(`${folder.value}/${fname}`).then(()=>{database.setMain(fname)});
});

export default defineComponent({
  components: {
    NavFolder, IconButton, InputField,
  },
  setup() {
    const filetree = ref<FileTree>();
    const inputfield = ref<typeof InputField|null>(null);

    function openProject(folder: string) {
      function inner() {
        const base = folder.substring(folder.lastIndexOf('/')+1);
        readDir(folder, {recursive: true}).then((entries) => {
          filetree.value = new FileTree(folder, base, entries);
          store.pdf.value.cwd = folder;
          database.importFromFileTree(filetree.value);
        });
      }

      exists(folder).then((yes)=>{
        if (yes) {
          const fw = FileWatcher(inner);
          fw.init(folder);
        }
      })
    }

    function newFile() {
      function inner(fname: string) {
        let path = `${folder.value}/${fname}`;
        console.log('creating file ', path);
        exists(path).then((yes) => {
          if (!yes) writeFile(path,'');
        })
      }
      if (folder.value!='') inputfield.value?.activate((arg:string)=>inner(arg));
    }

    function newFolder() {
      function inner(fname: string) {
        let path = `${folder.value}/${fname}`;
        console.log('creating folder ', path);
        exists(path).then((yes) => {
          if (!yes) createDir(path);
        })
      }
      if (folder.value!='') inputfield.value?.activate((arg:string)=>inner(arg));
    }

    onMounted(()=>{
      watchEffect(()=>{if (folder.value!='') openProject(folder.value)});
      wrapper('newfile', newFile);
      wrapper('newfolder', newFolder);
    })
    // onUnmounted(()=>{unlisten();});

    return {
      filetree,
      inputfield,
      reload() {openProject(folder.value);},
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