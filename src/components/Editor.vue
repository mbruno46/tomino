<template>
  <div style="height: 100%; background: var(--background-light);">
    <div class="tabbar">
      <tab-label v-for="(val, key) in files" :key="key" :open="val.open" :name="key">
      </tab-label>
    </div>
    <code-editor v-for="(val, key) in files" :path="val.path"
      :key="`code_${key}`" :class="val.open ? '': 'hide'"> -->
    </code-editor>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue'
import CodeEditor from './CodeEditor.vue';
import store from '@/helpers/Store'
import TabLabel from './TabLabel.vue';

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
.tabbar {
  display: flex;
  flex-direction: row;
  width: 100%;
  background: var(--background-dark);
}

.hide {
  visibility: hidden;
  opacity: 0;
}

</style>