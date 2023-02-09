<template>
  <div class="editor">
    <div class="tabbar">
      <tab-label v-for="(val, key) in files" :key="key" :open="val.open" :name="key.toString()">
      </tab-label>
    </div>
    <code-editor v-for="(val, key) in files" :path="val.path"
      :key="`code_${key}`" :class="val.open ? '': 'hide'"> -->
    </code-editor>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue'
import CodeEditor from '@/components/CodeEditor.vue';
import store from '@/helpers/Store'
import TabLabel from '@/components/TabLabel.vue';

export default defineComponent({
  components: { CodeEditor, TabLabel },
  setup() {
    const files = computed(() => store.Editor.files);

    return {
      files,
    }
  },
});
</script>

<style scoped>
.editor {
  height: 100%;
  width: 100%;
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