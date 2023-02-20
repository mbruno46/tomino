<template>
  <div class="browser">
    <div class="upperbar">
      <div class="title">PROJECT</div>
      <div class="buttons right">
        <icon-button :tag="'add-file'"></icon-button>
        <icon-button :tag="'add-folder'"></icon-button>
      </div>
    </div>
    <div class="filebrowser">
      <nav-folder v-if="filetree" :ftree="filetree"></nav-folder>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted, ref, watchEffect, computed } from 'vue'
import { readDir, exists } from '@tauri-apps/api/fs';
import { open } from '@tauri-apps/api/dialog';
import { listen } from '@tauri-apps/api/event';

import NavFolder from '@/components/NavFolder.vue';
import IconButton from '@/components/IconButton.vue';

import { FileTree } from '@/helpers/FileTree';
import store from '@/helpers/Store';
import database from '@/helpers/LatexData';

const folder = ref('');
const unlisten = await listen('openfolder', ()=>{
  open({directory: true, multiple: false, recursive: true}).then((dir) => {
    if ((dir!=null) && !Array.isArray(dir)) {
      folder.value = dir;
    }
  });
});

export default defineComponent({
  components: {
    NavFolder, IconButton,
  },
  setup() {
    const filetree = ref<FileTree>();

    function openProject(folder: string) {
      exists(folder).then((yes)=>{
        if (yes) {
          const base = folder.substring(folder.lastIndexOf('/')+1);
          readDir(folder, {recursive: true}).then((entries) => {
            filetree.value = new FileTree(folder, base, entries);
            database.importFromFileTree(filetree.value);
            store.pdf.value.cwd = folder;
          });
        }
      })
    }

    onMounted(()=>{
      watchEffect(()=>{if (folder.value!='') openProject(folder.value);})
    })
    onUnmounted(()=>{unlisten();});

    return {
      filetree,
    }
  },
});
</script>

<style scoped>
.browser {
  display: grid; 
  grid-template-rows: auto 1fr;
  height: 100%;
  overflow: hidden;
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