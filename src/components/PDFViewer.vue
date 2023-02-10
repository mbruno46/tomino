<template>
  <div ref="pdfviewer" class="pdfviewer">
    <div class="pdfpage" v-for="index in numpages" :index="index" :style="`width: ${width}px`">
      <canvas :id="`pdfpage_${index}`"></canvas>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watchEffect } from 'vue'
import * as pdfjsLib from "pdfjs-dist";
pdfjsLib.GlobalWorkerOptions.workerSrc = "../../node_modules/pdfjs-dist/build/pdf.worker.js";
import { readBinaryFile } from '@tauri-apps/api/fs';

export default defineComponent({
  setup() {
    let pages: pdfjsLib.PDFPageProxy[] = [];
    const scale = ref(4);
    var viewport = {aspect_ratio: 1, original_width: 1, zoom: 1};

    const numpages = ref(0);
    const width = ref(0);
    const pdfviewer = ref<HTMLDivElement|null>(null);

    function zoom(action: String) {
      if (!pdfviewer.value) {return}
      let old_zoom = viewport.zoom;

      if (action=='fitH') {
        width.value = pdfviewer.value.offsetWidth;
      } else if (action=='fitV') {
        width.value = pdfviewer.value.offsetHeight * viewport.aspect_ratio;
      } else if (action=='zoomIn') {
        if (viewport.zoom>6) {return}
        viewport.zoom *= 1.10;
        width.value = viewport.zoom * viewport.original_width;
      } else if (action=='zoomOut') {
        if (viewport.zoom>0.05) {return}
        viewport.zoom /= 1.10;
        width.value = viewport.zoom * viewport.original_width;
      }
      viewport.zoom = width.value / viewport.original_width;
      pdfviewer.value.scrollTop *= viewport.zoom / old_zoom;
      pdfviewer.value.scrollLeft *= viewport.zoom / old_zoom;

      if (viewport.zoom<2) scale.value = 4;
      else if (viewport.zoom>2 && viewport.zoom<4) scale.value = 8;
      else if (viewport.zoom>4) scale.value = 12;
    };

    function load(callback: Function) {
      readBinaryFile('/Users/mbruno/Physics/ToM/dummy/main.pdf').then((data) => {
        pdfjsLib.getDocument(data).promise.then((pdfDoc: any) => {
          numpages.value = pdfDoc.numPages;

          pages = [];
          for (let i = 0; i < pdfDoc.numPages; i++) {
            pdfDoc.getPage(i+1).then((page: pdfjsLib.PDFPageProxy) => {
                pages.push(page);
                renderPage(page, scale.value);
                callback();
            });
          }
        });
      });
    }

    function renderPage(page: pdfjsLib.PDFPageProxy, scale: number) {
      let canvas = document.getElementById(`pdfpage_${pages.indexOf(page)+1}`) as HTMLCanvasElement;

      var _viewport = page.getViewport({scale: scale});
      // Prepare canvas using PDF page dimensions
      var context = canvas.getContext('2d');
      canvas.width = _viewport.width;
      canvas.height = _viewport.height;
      viewport.aspect_ratio = _viewport.width / _viewport.height;
      viewport.original_width = _viewport.width;
      
      // Render PDF page into canvas context
      if (context) {
        var renderContext = {
          canvasContext: context, 
          viewport: _viewport
        };
        page.render(renderContext);
        console.log('page rendered')
      }
    }

    onMounted(() => {
      load(()=>zoom('fitH'));

      watchEffect(() => {
        for (const page of pages) renderPage(page, scale.value)
      })
    });

    return {
      numpages,
      pdfviewer,
      width,
      zoom,
    }
  },
})
</script>

<style scoped>
.pdfviewer {
  background-color: var(--background);
  overflow-y: scroll;
  overflow-y: scroll;
  text-align: center;
}

.pdfpage {
  padding: 1rem;
  justify-content: center;
}

.pdfpage canvas {
  width: 100%;
}
</style>