<template>
  <div class="browser">
    <div class="upperbar">
      <div style="width: min-content" class="padding">Browser</div>
    </div>
    <div class="filebrowser">
      <nav-folder v-if="filetree" :ftree="filetree"></nav-folder>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onBeforeMount, ref } from 'vue'
import { readDir } from '@tauri-apps/api/fs';
import { basename } from '@tauri-apps/api/path';
import { open } from '@tauri-apps/api/dialog';

import NavFolder from '@/components/NavFolder.vue';
import { FileTree } from '@/helpers/FileTree';
import store from '@/helpers/Store';

export default defineComponent({
  components: {
    NavFolder,
  },
  setup() {
    const filetree = ref<FileTree>();

    onBeforeMount(() => {
      open({directory: true, multiple: false, recursive: true}).then((folder) => {
        if ((folder!=null) && !Array.isArray(folder)) {
          const base = folder.substring(folder.lastIndexOf('/')+1);
          console.log(base, folder);
          readDir(folder, {recursive: true}).then((entries) => {
            filetree.value = new FileTree(folder, base, entries);
            store.pdf.value.cwd = folder;
            store.pdf.value.main = 'main';
          });
        }
      });
    });

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
  overflow: scroll;
}

.upperbar {
  width: 100%;
  height: 2rem;
}

.filebrowser {
  color: var(--foreground);
  height: max-content;
}

.right {
  float: right;
}
</style>