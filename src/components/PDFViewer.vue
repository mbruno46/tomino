<template>
  <div ref="pdfviewer" class="pdfviewer">
    <div class="pdfpage" v-for="index in numpages" :index="index" :style="`width: ${width}px`">
      <canvas :id="`pdfpage_${index}`" @dblclick="$emit('synctex', index, getViewportXY($event))"></canvas>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watchEffect } from 'vue'
import * as pdfjsLib from "pdfjs-dist";
pdfjsLib.GlobalWorkerOptions.workerSrc = "@/../node_modules/pdfjs-dist/build/pdf.worker.js";
import { readBinaryFile, exists } from '@tauri-apps/api/fs';
import store from '@/helpers/Store';

export default defineComponent({
  emits: ['synctex'],
  setup() {
    let pages: pdfjsLib.PDFPageProxy[] = [];
    let scale = 4;
    var viewport = {aspect_ratio: 1, original_width: 1, zoom: -1};

    const numpages = ref(0);
    const width = ref(0);
    const pdfviewer = ref<HTMLDivElement|null>(null);

    function zoom(action: String) {
      if (!pdfviewer.value) {return}
      if (viewport.zoom==-1) {viewport.zoom = width.value / viewport.original_width;}
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
        if (viewport.zoom<0.05) {return}
        viewport.zoom /= 1.10;
        width.value = viewport.zoom * viewport.original_width;
      }
      viewport.zoom = width.value / viewport.original_width;
      pdfviewer.value.scrollTop *= viewport.zoom / old_zoom;
      pdfviewer.value.scrollLeft *= viewport.zoom / old_zoom;

      if (viewport.zoom<2) scale = 4;
      else if (viewport.zoom>2 && viewport.zoom<4) scale = 8;
      else if (viewport.zoom>4) scale = 12;
    };

    function load(cwd: string, name: string) {
      let fname = `${cwd}/${name}.pdf`;
      if (!exists(fname)) {return;}
      
      readBinaryFile(fname).then((data) => {
        pdfjsLib.getDocument(data).promise.then((pdfDoc: any) => {
          numpages.value = pdfDoc.numPages;

          pages = [];
          for (let i = 0; i < pdfDoc.numPages; i++) {
            pdfDoc.getPage(i+1).then((page: pdfjsLib.PDFPageProxy) => {
              pages.push(page);
              renderPage(page, scale);
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
      width.value = pdfviewer.value!.offsetWidth;

      watchEffect(()=>{
        let pdf = store.pdf.value;
        if (pdf.refresh) {
          load(pdf.cwd, pdf.main);
          pdf.refresh = false;
        }
      })
    });

    return {
      numpages,
      pdfviewer,
      width,
      zoom,
      load,
      getViewportXY(event: MouseEvent) {
        let el = event.currentTarget as HTMLElement;
        let x = (event.offsetX / el.offsetWidth) * (viewport.original_width / scale ); 
        let y = (event.offsetY / el.offsetHeight) * (viewport.original_width / viewport.aspect_ratio / scale ); 
        return {x: x, y: y};
      }
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