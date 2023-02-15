<template>
  <div class="viewer">
    <div class="toolbar">
      <icon-button :tag="'fitH'" @click="pdfviewer?.zoom('fitH')"></icon-button>
      <icon-button :tag="'fitV'" @click="pdfviewer?.zoom('fitV')"></icon-button>
      <icon-button :tag="'+'" @click="pdfviewer?.zoom('zoomIn')"></icon-button>
      <icon-button :tag="'-'" @click="pdfviewer?.zoom('zoomOut')"></icon-button>
    </div>
    <PDFViewer ref="pdfviewer"></PDFViewer>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watchEffect } from 'vue'
import PDFViewer from '@/components/PDFViewer.vue';
import IconButton from '@/components/IconButton.vue';
import store from '@/helpers/Store';
import { Command } from '@tauri-apps/api/shell';

export async function compile(cwd: string, name: string, callback: Function) {
  const output = await new Command('latexmk', ['-pdf', '-silent', name], {cwd: cwd}).execute();
  if (output.code==0) {
    console.log('compiled ', output.stdout);
    callback();
  } else {
    console.log(output.stderr);
  }
}

export default defineComponent({
  components: {
    PDFViewer,
    IconButton,
  },
  setup() {
    const pdfviewer = ref<typeof PDFViewer|null>(null);

    onMounted(() => {
      watchEffect(() => {
        let pdf = store.pdf.value;
        if (pdf.compile) {
          compile(pdf.cwd, pdf.main, ()=>{pdf.refresh=true})
        }
      });
    });

    return {
      pdfviewer,
    }
  },
})
</script>

<style scoped>
.viewer {
  background-color: var(--background);
  height: 100vh;
  width: 100%;
  display: grid;
  grid-template-rows: min-content 1fr;
}

.toolbar {
  text-align: center;
  box-shadow: 0px 4px 6px 2px var(--background-dark);
}
</style>