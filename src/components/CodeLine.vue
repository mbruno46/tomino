<template>
  <div class="line" contenteditable="true">
    <div class="number">
      {{ (index+1) }}
    </div>
    <div ref="code" class="code" v-bind:linenumber="index" contenteditable="true">
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watchEffect } from 'vue'

function textToHTML(text: String) {
  if (text=="") {
    return "<br>";
  }

  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;")
    .replace(/\s/g, "&#8197;");
    // .replace(/\s/g, "&nbsp;");
}


function highlightTeX(text: String) {
  if (text.match(/^\s*%/)) {
    return `<span style="color: var(--latex-comment)">${textToHTML(text)}</span>`
  }
  let keywords = '\\\\' + ['begin','end','documentclass'].join('|\\\\');

  return textToHTML(text)
    .replace(RegExp(`(${keywords})\\[(.*?)\\]{(.*?)}`),'$1[<span style="color: var(--latex-square)">$2</span>]{<span style="color: var(--latex-curly)">$3</span>}')
    .replace(RegExp(`(${keywords}){(.*?)}`),'$1{<span style="color: var(--latex-curly)">$2</span>}')
    .replace(/(\\[a-zA-Z]+)/g,'<span style="color: var(--latex-basic)">$1</span>')
}

export default defineComponent({
  props: {
    index: {type: Number, default: 0},
    text: {type: String, default: ''},
  },
  setup(props) {
    const code = ref<HTMLDivElement | null>(null);

    onMounted(() => {
      watchEffect(() => {
        code.value!.innerHTML = highlightTeX(props.text);
      })
    })

    return {
      code,
    }
  },
})
</script>

<style scoped>
.line {
  display: grid;
  grid-template-columns: 4rem 1fr;
  width: 100%;
  height: max-content;
}

.number {
  width: 4rem;
  text-align: right;
  padding-right: 0.5rem;
  height: 100%;
  color: var(--foreground);
  -moz-user-select: none;
  -khtml-user-select: none;
  -webkit-user-select: none;
  -o-user-select: none;  
  user-select: none; 
}

.code {
  outline: none;
  /* white-space: normal; */
  word-wrap: break-word;
  color: var(--text);
  hyphens: auto;
  -webkit-hyphens:auto;
}

</style>
