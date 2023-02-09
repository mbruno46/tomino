<template>
  <aside>
  <div class="navitem">
    <span @click="handleClick">
      {{ name }}
    </span>
    <div :class="properties.isOpen ? '': 'nested'">
      <nav-item v-for="f in children" :key="f.path" 
      :path="f.path" :name="f.name" :children="f.children"></nav-item>
    </div>
  </div>
  </aside>
</template>

<script lang="ts">
import type { FileEntry } from '@tauri-apps/api/fs'
import { defineComponent, onMounted, ref } from 'vue'

interface TreeItem {
  path: String;
  name: String;
  children: FileEntry[]|undefined;
}

export default defineComponent({
  props: {
    path: String,
    name: String,
    children: {
      type: Object,
      // default(rawProps: Object) {
      //   return {};
      // }
    }
  },
  setup(props) {
    const properties = ref({isDir: false, isOpen: false});

    onMounted(() => {
      properties.value.isDir = props.children!=undefined
    });

    function handleClick(event: MouseEvent) {
      console.log(props.name, properties.value)
      if (properties.value.isDir) {
        properties.value.isOpen = !properties.value.isOpen;
      } else {
        console.log('fire open ', props.path)
      }
    }
    return {
      properties,
      handleClick,
    }
  },
})
</script>

<style scoped>
aside {
  width: 1rem;
}

.navitem {
  width: 100%;
  cursor: pointer;
}

.nested {
  display: none;
}

</style>