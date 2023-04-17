<template>
  <nav-label @click="expand = !expand" 
    :icon="(expand) ? 'down' : 'right'" :name="folder?.name"></nav-label>
  <div class="nav-folder" :class="(expand) ? '' : 'nested'">
    <nav-folder v-for="sf in folder?.subfolders" :key="sf.path" :folder="sf"></nav-folder>
    <nav-label v-for="f in folder?.files" :key="f.path" :name="f.name" 
      @click="openFile(f.path, f.name)" :ismain="f.name==main">
    </nav-label>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import type { PropType } from 'vue'
import NavLabel from './NavLabel.vue';
// import type { FileTree } from '@/helpers/FileTree';
import store from '@/helpers/Store';
import type { Folder } from '@/helpers/FileSystem';

export default defineComponent({
  components: {
    NavLabel,
  },
  props: {
    folder: {
      type: Object as PropType<Folder>,
    },
  },
  setup(props) {
    const expand = ref(true);
    const main = computed(()=>store.pdf.value.main+'.tex');
    return {
      expand,
      main
    }
  },
  methods:{
    openFile(path: String, name: String) {
      var ext = name.substring(name.lastIndexOf('.')+1);
      if (['tex','bib','bbl'].includes(ext)) { 
        store.Editor.openFile(path as string, name as string);
      }
    },
  }
})
</script>

<style scoped>
.nav-folder {
  display: flex;
  flex-flow: column;
  padding-left: 1rem;
}

.nested {
  display: none;
}

.nav-folder div {
  border: 1px solid transparent;
}

.nav-folder > .nav-label:hover {
  cursor: pointer;
  background-color: var(--background-light);
  color: var(--text);
  border: 1px solid var(--selection-dark);
}
</style>

