<template>
  <div class="viewer">
    <div class="toolbar">
      <icon-button :tag="'fitH'" @click="pdfviewer?.zoom('fitH')"></icon-button>
      <icon-button :tag="'fitV'" @click="pdfviewer?.zoom('fitV')"></icon-button>
      <icon-button :tag="'+'" @click="pdfviewer?.zoom('zoomIn')"></icon-button>
      <icon-button :tag="'-'" @click="pdfviewer?.zoom('zoomOut')"></icon-button>
    </div>
    <PDFViewer v-if="error==''" ref="pdfviewer"></PDFViewer>
    <PDFError v-else>{{ error }}</PDFError>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watchEffect, onUnmounted } from 'vue'
import PDFViewer from '@/components/PDFViewer.vue';
import PDFError from '@/components/PDFError.vue';
import IconButton from '@/components/IconButton.vue';
import store from '@/helpers/Store';
import { Command } from '@tauri-apps/api/shell';
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen('recompile', ()=>{
  store.pdf.value.compile = true;
});

export async function compile(cwd: string, name: string, callback: Function, error: Function) {
  const output = await new Command('latexmk', ['-pdf', '-silent', name], {cwd: cwd}).execute();
  console.log('compiling');
  if (output.code==0) {
    console.log('compiled ', output.stdout);
    callback();
  } else {
    console.log(output.stderr);
    error(output.stderr);
  }
  store.pdf.value.compile = false;
}

export default defineComponent({
  components: {
    PDFViewer,
    IconButton,
    PDFError,
  },
  setup() {
    const pdfviewer = ref<typeof PDFViewer|null>(null);
    const error = ref('');

    onMounted(() => {
      watchEffect(() => {
        let pdf = store.pdf.value;
        console.log(pdf)
        if (pdf.compile) {
          compile(pdf.cwd, pdf.main, 
            ()=>{
              pdf.refresh=true;
              error.value = '';
            }, 
            (arg:string)=>{
              error.value = arg;
            }
          )
        }
      });
    });
    onUnmounted(()=>{unlisten();});

    return {
      pdfviewer,
      error,
    }
  },
})
</script>

<style scoped>
.viewer {
  background-color: var(--background);
  height: 100%;
  display: grid;
  grid-template-rows: auto 1fr;
  overflow: hidden;
}

.toolbar {
  text-align: center;
  box-shadow: 0px 10px 8px -8px var(--background-dark);
  position: relative;
}
</style>