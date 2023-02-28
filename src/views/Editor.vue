<template>
  <div class="editor">
    <div class="tabbar">
      <tab-label v-for="(val, key) in files" :key="key" 
        :open="val.open" :modified="val.modified" :name="key.toString()">
      </tab-label>
    </div>
    <code-editor v-for="(val, key) in files" :path="val.path"
      :key="`code_${key}`" :class="val.open ? '': 'hide'" :ref="(el)=>setCodeEditorRef(el, key.toString())"
      @status="(n)=>{getStatus(key.toString(),n);}">
    </code-editor>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref, watchEffect } from 'vue'
import CodeEditor from '@/components/CodeEditor.vue';
import store from '@/helpers/Store'
import TabLabel from '@/components/TabLabel.vue';

export default defineComponent({
  components: { CodeEditor, TabLabel },
  setup() {
    const files = computed(() => store.Editor.files);
    const code_editors = ref<{[key:string]: any}>({});

    onMounted(()=>{
      watchEffect(()=>{
        let s = store.pdf.value.synctex;
        if (s.sync) {
          console.log(s);
          let name = s.path.substring(s.path.lastIndexOf('/')+1);
          store.Editor.openFile(s.path, name);
          code_editors.value[name].setSelection(s.line, s.column);
        }
      })
    });

    return {
      files,
      getStatus(name: string, status: number) {
        if (status==1) {files.value[name].modified = true}
        else if (status==2) {files.value[name].modified = false}
      },
      setCodeEditorRef(el: any, key: string) {
        code_editors.value[key] = el;
      },
    }
  },
});
</script>

<style scoped>
.editor {
  height: 100%;
  overflow: hidden;
  background: var(--background-light);
  position: relative;
}

.tabbar {
  display: flex;
  flex-direction: row;
  width: 100%;
  overflow-y: hidden;
  overflow-x: scroll;
  background: var(--background-dark);
}

.tabbar::-webkit-scrollbar {
  display: none;
}

.hide {
  visibility: hidden;
  opacity: 0;
}

</style>