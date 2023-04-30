<template>
  <nav-label @click="expand = !expand" 
    :icon="(expand) ? 'down' : 'right'" :name="name"></nav-label>
  <div class="nav-folder" :class="(expand) ? '' : 'nested'">
    <navigation-folder v-for="sf in subfolders" :key="sf" :path="sf"></navigation-folder>
    <nav-label v-for="f in files" :key="f" :name="getName(f)" 
      @click="openFile(f, getName(f))" :ismain="getName(f)==main">
    </nav-label>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'

import NavLabel from './NavLabel.vue';
import store from '@/helpers/Store';
import { Folder } from '@/helpers/LatexDB';

export default defineComponent({
  components: {
    NavLabel,
  },
  props: {
    path: String,
  },
  setup(props) {
    const expand = ref(true);
    const name = ref('');
    const main = computed(()=>store.pdf.value.main+'.tex');

    const getName = (path: string) => path.substring(path.lastIndexOf('/')+1);

    let folder = Folder();
    const subfolders = folder?.subfolders;
    const files = folder?.files;

    onMounted(()=>{
      if (props.path) {
        name.value = getName(props.path)
        folder.init(props.path);
      }
    })


    return {
      expand,
      subfolders,
      files,
      name,
      main,
      getName,
    }
  },
  methods:{
    openFile(path: String, name: String) {
      var ext = name.substring(name.lastIndexOf('.')+1);
      if (['tex','bib','bbl'].includes(ext)) { 
        store.Editor.openFile(path as string, name as string);
      }
    },
  }})
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
