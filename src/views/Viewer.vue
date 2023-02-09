<template>
  <div class="viewer">

  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue'
import * as pdfjsLib from "pdfjs-dist";
pdfjsLib.GlobalWorkerOptions.workerSrc = "../../node_modules/pdfjs-dist/build/pdf.worker.js";
import { readBinaryFile } from '@tauri-apps/api/fs';


export default defineComponent({
  setup() {
    onMounted(() => {
      readBinaryFile('/Users/mbruno/Physics/ToM/dummy/main.pdf').then((data) => {
        pdfjsLib.getDocument(data).promise.then((pdfDoc: any) => {
          console.log(pdfDoc.numPages);
        });
      });
    });
  },
})
</script>

<style scoped>
.viewer {
  background-color: var(--background);
  height: 100%;
}
</style>