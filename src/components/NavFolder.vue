<template>
  <nav-item @click="expand = !expand" 
    :icon="(expand) ? 'down' : 'right'">{{ ftree?.name }}</nav-item>
  <div class="nav-folder" :class="(expand) ? '' : 'nested'">
    <nav-folder v-for="sf in ftree?.subfolders" :key="sf.path" :ftree="sf">{{ sf.name }}</nav-folder>
    <nav-item v-for="f in ftree?.files" :key="f.path"
      :icon="getExt(f.name)" @click="openFile(f.path, f.name)">
      {{ f.name }}
    </nav-item>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import type { PropType } from 'vue'
import NavItem from './NavItem.vue';
import type { FileTree } from '../helpers/FileTree';
import store from '@/helpers/Store';

export default defineComponent({
  components: {
    NavItem,
  },
  props: {
    ftree: {
      type: Object as PropType<FileTree>,
    },
  },
  setup() {
    const expand = ref(true);
    return {
      expand,
    }
  },
  methods:{
    openFile(path: String, name: String) {
      var ext = this.getExt(name);
      if (['tex','bib','bbl'].includes(ext)) { 
        store.Editor.openFile(path as string, name as string);
      }
    },
    getExt(name: String) {
      return name.substring(name.lastIndexOf('.')+1)
    },
    // getIcon(name: String) {
    //   var ext = getExt(name);
    //   if (ext=='tex') {
    //     return 'ri-text';
    //   } else if (ext=='bib') {
    //     return 'ri-file-text-line';
    //   } else if (ext=='pdf') {
    //     return "ri-file-pdf-line"
    //   }
    //   return 'ri-file-line'
    // }
  }
})
</script>

<style scoped>
.nav-folder {
  display: flex;
  flex-flow: column;
  padding-left: 1rem;
  /* transition: height 0.2s; */
}

.nested {
  display: none;
  /* height: 0px; */
}

</style>

