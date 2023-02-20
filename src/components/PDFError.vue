<template>
  <div class="error" ref="errmsg">
    <span v-for="err in errmsg" v-html="textToHTML(err)" 
      :class="highlight(err) ? 'highlight-error' : ''" :key="err"></span>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'

export default defineComponent({
  props: {
    error: String,
  },
  setup(props) {
    const errmsg = computed(()=>props.error?.split('\n'));

    return {
      errmsg,
    }
  },
  methods: {
    highlight(text: string) {
      return text.match(/l\.\d+.*|Runaway\sargument|! LaTeX Error|I found no.*/)
    },
    textToHTML(text: String) {
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
    }
  }
});
</script>

<style scoped>
.error {
  width: 100%;
  overflow: scroll;
  display: flex;
  flex-direction: column;
}

.error span {
  width: fit-content;
}
.highlight-error {
  color: var(--orange);
  text-decoration: solid;
}
</style>