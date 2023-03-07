<template>
  <div ref="pdfviewer" class="pdfviewer" @scroll="handleScroll">
    <div class="pdfpage" v-for="index in numpages" :index="index" :style="`width: ${width}px`">
      <canvas :id="`pdfpage_${index}`" style="background-color: white;"
        @dblclick="$emit('synctex', index, getViewportXY($event))"></canvas>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watchEffect,  computed, onBeforeUpdate } from 'vue'
import { readBinaryFile, exists } from '@tauri-apps/api/fs';
import store from '@/helpers/Store';

import 'core-js';
import * as pdfjsLib from "pdfjs-dist";
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker?worker';

export default defineComponent({
  emits: ['synctex'],
  setup() {
    let scale = 2;
    var viewport = {aspect_ratio: 1, original_width: 1, zoom: -1};

    const numpages = ref(0);
    const width = ref(0);
    const pdfviewer = ref<HTMLDivElement|null>(null);

    function stretch(vertical: boolean) {
      if (!pdfviewer.value) {return}
      width.value = pdfviewer.value.offsetWidth * ((vertical) ? viewport.aspect_ratio : 1);
      viewport.zoom = width.value / viewport.original_width;
    }

    function zoom(zoomin: boolean) {
      if (!pdfviewer.value) {return}
      
      let f = (zoomin) ? 1.10 : 1/1.10;
      let neww = width.value * f;
      let zoom = neww /  viewport.original_width;
      if (zoom>6 || zoom<0.1) {return}
      
      // let zoom = width.value / old;
      // pdfviewer.value.scrollTop *= f;
      // pdfviewer.value.scrollLeft *= f;
      
      width.value = neww;
      scale = Math.floor(zoom)*2+2;
      console.log(zoom, scale, Math.floor(zoom/f)*2+2);
      // if (scale != Math.floor(zoom/f)*2+2) repaintPages();
    };

    let rendered = <number[]>[];
    let pages = <typeof pdfjsLib.PDFPageProxy[]>[];
    async function load(cwd: string, name: string) {
      let fname = `${cwd}/${name}.pdf`;
      if (!exists(fname)) {return;}
      
      const data = await readBinaryFile(fname);
      const pdfDoc = await pdfjsLib.getDocument(data).promise;
      numpages.value = pdfDoc.numPages;

      rendered = [];
      pages = [];
      for (let i = 0; i < pdfDoc.numPages; i++) {
        const page = await pdfDoc.getPage(i+1);
        pages.push(page);
        createPage(page, i);
      }
    }

    function createPage(page: any, index: number) {
      let canvas = document.getElementById(`pdfpage_${index+1}`) as HTMLCanvasElement;
      var _viewport = page.getViewport({scale: scale});
      canvas.width = _viewport.width;
      canvas.height = _viewport.height;
      viewport.aspect_ratio = _viewport.width / _viewport.height;
      viewport.original_width = _viewport.width;      
    }

    function renderPage(index: number) {
      if (rendered.includes(index)) return;

      let canvas = document.getElementById(`pdfpage_${index+1}`) as HTMLCanvasElement;
      let page = pages[index];

      var context = canvas.getContext('2d');
      if (context) {
        var renderContext = {
          canvasContext: context, 
          viewport: page.getViewport({scale: scale})
        };
        page.render(renderContext);
        rendered.push(index);
        console.log('page rendered')
      }      
    }

    function clearPage(index: number) {
      if (!rendered.includes(index)) return;

      let canvas = document.getElementById(`pdfpage_${index+1}`) as HTMLCanvasElement;
      var context = canvas.getContext('2d');
      context?.clearRect(0, 0, canvas.width, canvas.height);
      delete rendered[rendered.indexOf(index)];
    }

    function repaintPages() {
      console.log('repainting ', scale);
      for (const r of rendered) {
        clearPage(r);
        renderPage(r);
      }
    }

    function handleScroll() {
      if (pdfviewer.value==null) return;

      let el = pdfviewer.value;
      if (el.scrollTop<0) return;
      
      let pdfpage_height = width.value / viewport.aspect_ratio;
      let id0 = Math.floor(el.scrollTop/pdfpage_height)
      let id1 = Math.round((el.scrollTop + el.offsetHeight)/pdfpage_height);
      for (const r of rendered) if ((r<id0)||(r>id1)) clearPage(r);
      for (let i=id0; i<=id1; i++) renderPage(i);
    }
    
    onMounted(() => {
      pdfjsLib.GlobalWorkerOptions.workerPort = new pdfjsWorker();
      width.value = pdfviewer.value!.offsetWidth;

      watchEffect(async()=>{
        let pdf = store.pdf.value;
        if (pdf.refresh) {
          await load(pdf.cwd, pdf.main);
          handleScroll();
          pdf.refresh = false;
        }
      });
    });

    return {
      numpages,
      pdfviewer,
      width,
      stretch,
      zoom,
      load,
      handleScroll,
      getViewportXY(event: MouseEvent) {
        let el = event.currentTarget as HTMLElement;
        let x = (event.offsetX / el.offsetWidth) * (viewport.original_width / scale ); 
        let y = (event.offsetY / el.offsetHeight) * (viewport.original_width / viewport.aspect_ratio / scale ); 
        return {x: x, y: y};
      },
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