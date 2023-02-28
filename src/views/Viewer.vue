<template>
  <div class="viewer">
    <div class="toolbar">
      <icon-button :tag="'fitH'" @click="pdfviewer?.zoom('fitH')"></icon-button>
      <icon-button :tag="'fitV'" @click="pdfviewer?.zoom('fitV')"></icon-button>
      <icon-button :tag="'+'" @click="pdfviewer?.zoom('zoomIn')"></icon-button>
      <icon-button :tag="'-'" @click="pdfviewer?.zoom('zoomOut')"></icon-button>
    </div>
    <PDFViewer v-if="error==''" ref="pdfviewer" @synctex="syncTeX"></PDFViewer>
    <PDFError v-else :error="error"></PDFError>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watchEffect, onUnmounted } from 'vue'

import PDFViewer from '@/components/PDFViewer.vue';
import PDFError from '@/components/PDFError.vue';
import IconButton from '@/components/IconButton.vue';

import store from '@/helpers/Store';
import { SyncTex } from '@/helpers/SyncTex';
import { wrapper } from '@/helpers/Utils';

import { Command } from '@tauri-apps/api/shell';
import { readTextFile, exists } from '@tauri-apps/api/fs';

wrapper('recompile1', ()=>{
  store.pdf.value.compile = 1;
});
wrapper('recompile2', ()=>{
  store.pdf.value.compile = 2;
});

let sync = SyncTex();

export default defineComponent({
  components: {
    PDFViewer,
    IconButton,
    PDFError,
  },
  setup() {
    const pdfviewer = ref<typeof PDFViewer|null>(null);
    const error = ref('');

    async function compile(cwd: string, name: string, level:number=1) {
      store.pdf.value.loader = true;

      let args = ['-pdf', '-silent','-synctex=-1'];
      if (level==2) {
        args.push('-g');
        args.push('-f');
      }
      args.push(name);
      const output = await new Command('latexmk', args, {cwd: cwd}).execute();

      if (output.code==0) {
        console.log('compiled ', output.stdout);
        store.pdf.value.refresh=true;
        error.value = '';
        
        readTextFile(`${store.pdf.value.cwd}/${store.pdf.value.main}.synctex`).then(
          (content)=>sync.parse(content)
        );
      } else {
        console.log(output.stderr);
        // error.value = output.stdout + '\n' + output.stderr;
        if (output.stderr.match(/bibtex main: Bibtex errors: See file 'main.blg'/)) {
          let fname = `${store.pdf.value.cwd}/${store.pdf.value.main}.blg`
          exists(fname).then(()=>{
            readTextFile(fname).then((content) => error.value = content)
          })
        } else {
          let fname = `${store.pdf.value.cwd}/${store.pdf.value.main}.log`
          exists(fname).then(()=>{
            readTextFile(fname).then((content) => error.value = content)
          })          
        }
      }
      store.pdf.value.compile = 0;
      store.pdf.value.loader = false;
    }

    onMounted(() => {
      watchEffect(() => {
        let pdf = store.pdf.value;
        if (pdf.compile>0) exists(`${pdf.cwd}/${pdf.main}.tex`).then(()=>compile(pdf.cwd, pdf.main, pdf.compile));
      });
    });
    // onUnmounted(()=>{unlisten1(); unlisten2();});

    return {
      pdfviewer,
      error,
      syncTeX(pageid: number, xy: {x:0, y:0}) {
        store.pdf.value.synctex = sync.pdf2tex(pageid, xy.x, xy.y);
      }
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