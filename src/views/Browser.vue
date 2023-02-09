<template>
  <div class="browser">
    <div class="upperbar">
      <div style="width: min-content" class="padding">Browser</div>
    </div>
    <div class="filebrowser">
      <nav-folder v-if="render" :ftree="filetree"></nav-folder>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onBeforeMount, ref } from 'vue'
import { readDir } from '@tauri-apps/api/fs';
import { open } from '@tauri-apps/api/dialog';
import NavFolder from '@/components/NavFolder.vue';
import { FileTree } from '@/helpers/FileTree';
import store from '@/helpers/Store';

export default defineComponent({
  components: {
    NavFolder,
  },
  setup() {
    const render = ref(false);
    const filetree = ref<FileTree>();

    onBeforeMount(() => {
      // open({directory: true, multiple: false, recursive: true}).then((folder) => {
      //   if ((folder!=null) && !Array.isArray(folder)) {
      //     readDir(folder, {recursive: true}).then((entries) => {
      //       filetree.value = new FileTree(folder, 'main', entries);
      //       render.value = true;
      //     });
      //   }
      // });
      readDir("/Users/mbruno/Physics/ToM/dummy", {recursive: true}).then((entries) => {
        filetree.value = new FileTree("/Users/mbruno/Physics/ToM/dummy", 'main', entries);
        render.value = true;
      });
    });

    return {
      filetree,
      render,
    }
  },
  methods: {
    hide() {
      store.browser.value.visible = false;
    }
  }
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
  color: var(--text);
  height: max-content;
}

.right {
  float: right;
}
</style>