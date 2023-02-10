import { ref } from 'vue';
import * as pdfjsLib from "pdfjs-dist";
pdfjsLib.GlobalWorkerOptions.workerSrc = "../../node_modules/pdfjs-dist/build/pdf.worker.js";
import { readBinaryFile } from '@tauri-apps/api/fs';


function _viewer() {
  const pages = ref<pdfjsLib.PDFPageProxy[]>([]);
  var scale = 0.2;
  var aspect_ratio = 1;

  function load() {
    readBinaryFile('/Users/mbruno/Physics/ToM/dummy/main.pdf').then((data) => {
      pdfjsLib.getDocument(data).promise.then((pdfDoc: any) => {
        pages.value = [];
        for (let i = 0; i < pdfDoc.numPages; i++) {
          pdfDoc.getPage(i+1).then((page: pdfjsLib.PDFPageProxy) => {
            pages.value.push(page);
          });
        }
      });
    });
  }

  function renderPage(canvas: HTMLCanvasElement, index: number) {
    let page = pages.value[index];

    var viewport = page.getViewport({scale: scale});
    console.log(viewport.width/ scale, viewport.height/scale, )
    // Prepare canvas using PDF page dimensions
    var context = canvas.getContext('2d');
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    aspect_ratio = viewport.width / viewport.height;
    
    // Render PDF page into canvas context
    if (context) {
      var renderContext = {
        canvasContext: context, 
        viewport: viewport
      };
      page.render(renderContext);
      console.log('page rendered')
    }
  }

  return {
    pages,
    load,
    renderPage,
  }
}

var Viewer = _viewer();
export default Viewer;

// export default {
//   Viewer,
// }