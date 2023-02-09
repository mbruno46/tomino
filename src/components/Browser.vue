<template>
  <div style="display: grid; grid-template-rows: auto 1fr;">
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
import NavFolder from './NavFolder.vue';
import { FileTree } from '../helpers/FileTree';
import store from '../helpers/Store';

const folder = '/Users/mbruno/Physics/ToM/dummy';


export default defineComponent({
  components: {
    NavFolder,
  },
  setup() {
    const render = ref(false);
    const filetree = ref<FileTree>();

    onBeforeMount(() => {
      readDir(folder, {recursive: true}).then((entries) => {
        filetree.value = new FileTree(folder, 'main', entries);
        render.value = true;
        console.log(filetree.value);
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
.upperbar {
  width: 100%;
  height: 2rem;
  /* display: grid; */
  /* grid-template-columns: min-content; */
}

.filebrowser {
  color: var(--text);
  height: max-content;
}

.right {
  float: right;
}
</style>