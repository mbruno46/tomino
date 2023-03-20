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
    let renderpages = <number[]>[];

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
      render(true);
    }

    function zoom(zoomin: boolean) {
      if (!pdfviewer.value) {return}
      
      let f = (zoomin) ? 1.10 : 1/1.10;
      width.value = round(width.value * f);
      pdfviewer.value.scrollTop = pdfviewer.value.scrollTop * f  + pdfviewer.value.offsetHeight * (f-1) * 0.5;
      pdfviewer.value.scrollLeft = pdfviewer.value.scrollLeft * f  + pdfviewer.value.offsetWidth * (f-1) * 0.5;
    }

    let pages = <any[]>[];
    async function load(cwd: string, name: string) {
      let fname = `${cwd}/${name}.pdf`;
      if (!exists(fname)) {return;}
      
      const data = await readBinaryFile(fname);
      const pdfDoc = await pdfjsLib.getDocument(data).promise;
      numpages.value = pdfDoc.numPages;

      pages = [];

      for (let i = 0; i < pdfDoc.numPages; i++) {
        const page = await pdfDoc.getPage(i+1);
        if (i==0) initViewport(page);
        pages.push(page);
      }
    }

    function initViewport(page: any) {
      var _viewport = page.getViewport({scale: 1});
      viewport.height = _viewport.height; 
      viewport.width = _viewport.width;
    }

    function render(force = false) {
      function setCanvas() {
        for (let i=0; i<pages.length; i++) {
          let canvas = document.getElementById(`pdfpage_${i+1}`) as HTMLCanvasElement;
          canvas.getContext('2d')?.clearRect(0, 0, canvas.width, canvas.height);

          var _viewport = pages[i].getViewport({scale: scale});
          canvas.width = _viewport.width;
          canvas.height = _viewport.height;
        }
      }

      // adapt scale and reset canvas if needed (first load + zoom)
      let shouldRender = false;
      let r = Math.round(width.value/viewport.width/0.5+1)*0.5;
      r = (r<1) ? 1 : ((r>4) ? 4 : r);
      if (scale!=r || force) {
        scale = r;
        setCanvas();
        shouldRender = true;
      }

      // update pages in viewport
      let oldr = [...renderpages];
      updatePagesInViewport();

      // clear pages out of viewport
      for (const i of oldr) {
        if (!renderpages.includes(i)) clearPage(i);
      }
        
      for (const i of renderpages) {
        if (shouldRender || !oldr.includes(i)) renderPage(i);
      }
    }


    function renderPage(index: number) {
      let page = pages[index];
      let canvas = document.getElementById(`pdfpage_${index+1}`) as HTMLCanvasElement;
      console.log('r', index, canvas)

      var context = canvas.getContext('2d');
      context?.clearRect(0, 0, canvas.width, canvas.height);

      if (context) {
        var renderContext = {
          canvasContext: context, 
          viewport: page.getViewport({scale: scale})
        };
        page.render(renderContext);
        console.log('page rendered')
      }
    }

    function clearPage(index: number) {
      let canvas = document.getElementById(`pdfpage_${index+1}`) as HTMLCanvasElement;
      if (canvas) {
        console.log('c',index, canvas)
        var context = canvas.getContext('2d');
        context?.clearRect(0, 0, canvas.width, canvas.height);
      }
    }

    function updatePagesInViewport() {
      if (pdfviewer.value==null) return;
      let el = pdfviewer.value;
      if (el.scrollTop<0) return;
      
      let height = width.value * (viewport.height / viewport.width);
      let id0 = Math.floor(el.scrollTop/height)
      let id1 = Math.round((el.scrollTop + el.offsetHeight)/height);

      let r = renderpages;
      // removes pages out of viewport
      for (const i of [...r]) if ((i<id0)||(i>id1)||(i>numpages.value-1)) r.splice(r.indexOf(i), 1);
      // adds pages in viewport
      for (let i=id0; i<=Math.min(id1, numpages.value-1); i++) if (!r.includes(i)) r.push(i);
    }
    
    onMounted(() => {
      pdfjsLib.GlobalWorkerOptions.workerPort = new pdfjsWorker();
      stretch(true);

      watchEffect(async()=>{
        let pdf = store.pdf.value;
        if (pdf.refresh) {
          await load(pdf.cwd, pdf.main);
          render(true);
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
      handleScroll() {
        render();
      },
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