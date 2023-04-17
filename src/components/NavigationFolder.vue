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
import type { Ref } from 'vue'
import { defineComponent, ref, computed, onMounted } from 'vue'
import { readDir } from '@tauri-apps/api/fs';

import NavLabel from './NavLabel.vue';
import store from '@/helpers/Store';
import { TimeStamp } from '@/helpers/Utils';

function pop<T>(arr: Ref<T[]>, item:T) {
  let idx = arr.value.indexOf(item);
  arr.value.splice(idx, 1);
}

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
    const subfolders = ref<string[]>([]);
    const files = ref<string[]>([]);
    const main = computed(()=>store.pdf.value.main+'.tex');
    let timestamp = 0;

    function update() {
      readDir(props.path!, {recursive: false}).then((entries)=>{
        let keep = <string[]>[]

        for (const c of entries) {
          if (!c.name) continue;
          if (c.name?.substring(0,1)=='.') continue;

          if (c.children) {
            if (!(subfolders.value.includes(c.path))) subfolders.value.push(c.path);
          } else {
            if (!(files.value.includes(c.path))) files.value.push(c.path);
            // if (files.value.includes(c.path)) {
            //   TimeStamp(c.path, (t:number)=>{if (t>=timestamp) {
            //     // timestamp = t;
            //     database.update(c.path)
            //   }
            //   });
            // } else {
            //   files.value.push(c.path);
            //   database.update(c.path);
            // }
          }

          keep.push(c.path);
        }

        // clean
        for (var f of files.value) if (!keep.includes(f)) pop(files, f);
        for (var sf of subfolders.value) if (!keep.includes(sf)) pop(subfolders, sf);

        TimeStamp(props.path!, (t:number)=>{timestamp=t});
      })
    }

    const getName = (path: string) => path.substring(path.lastIndexOf('/')+1);

    onMounted(()=>{
      if (props.path) {
        name.value = getName(props.path)
        update();

        setInterval(()=>TimeStamp(props.path!, (t:number) => {if (t>timestamp) update();}), 3000);        
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
