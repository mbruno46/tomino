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
import { defineComponent, onMounted, ref } from 'vue'
import PDFViewer from '@/components/PDFViewer.vue';
import IconButton from '@/components/IconButton.vue';

export default defineComponent({
  components: {
    PDFViewer,
    IconButton,
  },
  setup() {
    const pdfviewer = ref<typeof PDFViewer|null>(null);

    onMounted(() => {
      // if (pdfviewer.value) pdfviewer.value.performAction('fitH');
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
  grid-template-rows: fit-content 1fr;
}

.toolbar {
  text-align: center;
  /* border-bottom: 2px solid black; */
  /* box-shadow: 0px 15px 10px -15px #111; */
}
</style>