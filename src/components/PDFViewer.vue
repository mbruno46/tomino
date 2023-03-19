<template>
  <div ref="pdfviewer" class="pdfviewer" @scroll="handleScroll">
    <canvas v-for="index in numpages" class="pdfpage" 
      :id="`pdfpage_${index}`" 
      :style="`width: ${width}px`"
      @dblclick="$emit('synctex', index, getViewportXY($event))">
    </canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watchEffect } from 'vue'
import { readBinaryFile, exists } from '@tauri-apps/api/fs';
import store from '@/helpers/Store';

import 'core-js';
import * as pdfjsLib from "pdfjs-dist";
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker?worker';

export default defineComponent({
  emits: ['synctex'],
  setup() {
    let scale = 0;
    var viewport = {height: 1, width: 1};

    const numpages = ref(0);
    const width = ref(0);
    const pdfviewer = ref<HTMLDivElement|null>(null);

    const round = (x: number) => Math.round(x)

    function stretch(horizontal: boolean) {
      if (!pdfviewer.value) {return}
      if (horizontal) {
        width.value = round(pdfviewer.value.offsetWidth);
      } else {
        width.value = round(pdfviewer.value.offsetHeight * viewport.width / viewport.height)
      }
    }

    function zoom(zoomin: boolean) {
      if (!pdfviewer.value) {return}
      
      let f = (zoomin) ? 1.10 : 1/1.10;
      width.value = round(width.value * f);
      pdfviewer.value.scrollTop = pdfviewer.value.scrollTop * f  + pdfviewer.value.offsetHeight * (f-1) * 0.5;
      pdfviewer.value.scrollLeft = pdfviewer.value.scrollLeft * f  + pdfviewer.value.offsetWidth * (f-1) * 0.5;
    }

    let rendered = <number[]>[];
    let pages = <any[]>[];
    async function load(cwd: string, name: string) {
      let fname = `${cwd}/${name}.pdf`;
      if (!exists(fname)) {return;}
      
      const data = await readBinaryFile(fname);
      const pdfDoc = await pdfjsLib.getDocument(data).promise;
      numpages.value = pdfDoc.numPages;

      // rendered = [];
      pages = [];

      for (let i = 0; i < pdfDoc.numPages; i++) {
        const page = await pdfDoc.getPage(i+1);
        if (i==0) initViewport(page);
        pages.push(page);
        // checkCanvas(i, page, true);
      }
      scale = 1;
      resetCanvas();
    }

    function initViewport(page: any) {
      var _viewport = page.getViewport({scale: 1});
      viewport.height = _viewport.height; 
      viewport.width = _viewport.width;
    }

    function resetCanvas() {
      for (let i=0; i<pages.length; i++) {
        let canvas = document.getElementById(`pdfpage_${i+1}`) as HTMLCanvasElement;
        canvas.getContext('2d')?.clearRect(0, 0, canvas.width, canvas.height);

        var _viewport = pages[i].getViewport({scale: scale});
        canvas.width = _viewport.width;
        canvas.height = _viewport.height;
      }
    }

    function checkCanvas(index: number, page: any) {
      let r = Math.round(width.value/viewport.width/0.5+1)*0.5;
      r = (r<1) ? 1 : ((r>4) ? 4 : r);
      if (scale!=r) {
        scale = r;
        resetCanvas();
        return true;
      }
      return false;
    }


    function renderPage(index: number) {
      let page = pages[index];
      let shouldRender = (checkCanvas(index, page)) ? true : !rendered.includes(index);
      if (!shouldRender) return;

      let canvas = document.getElementById(`pdfpage_${index+1}`) as HTMLCanvasElement;
      console.log('r', index, canvas)

      var context = canvas.getContext('2d');
      if (context) {
        var renderContext = {
          canvasContext: context, 
          viewport: page.getViewport({scale: scale})
        };
        page.render(renderContext);
        console.log('page rendered')
      }

      if (!rendered.includes(index)) rendered.push(index);
    }

    function clearPage(index: number) {
      let canvas = document.getElementById(`pdfpage_${index+1}`) as HTMLCanvasElement;
      console.log('c',index, canvas)
      var context = canvas.getContext('2d');
      context?.clearRect(0, 0, canvas.width, canvas.height);
      rendered.splice(rendered.indexOf(index), 1);
    }

    function handleScroll() {
      if (pdfviewer.value==null) return;
      let el = pdfviewer.value;
      if (el.scrollTop<0) return;
      
      let height = width.value * (viewport.height / viewport.width);
      let id0 = Math.floor(el.scrollTop/height)
      let id1 = Math.round((el.scrollTop + el.offsetHeight)/height);
      for (const r of [...rendered]) if ((r<id0)||(r>id1)) clearPage(r);
      for (let i=id0; i<=Math.min(id1, numpages.value-1); i++) renderPage(i);
    }
    
    onMounted(() => {
      pdfjsLib.GlobalWorkerOptions.workerPort = new pdfjsWorker();
      stretch(true);

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
        let x = (event.offsetX / el.offsetWidth) * viewport.width; 
        let y = (event.offsetY / el.offsetHeight) * viewport.height; 
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
  overflow-x: scroll;
  text-align: center;
}

.pdfpage {
  padding: 1rem;
  justify-content: center;
}
</style>