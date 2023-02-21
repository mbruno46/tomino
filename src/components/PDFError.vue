<template>
  <div class="error" ref="pdferror">
    <span v-for="err in errmsg" v-html="textToHTML(err)" 
      :class="highlight(err) ? 'highlight-error' : ''" :key="err"></span>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onUpdated, ref, onMounted } from 'vue'

export default defineComponent({
  props: {
    error: String,
  },
  setup(props) {
    const errmsg = computed(()=>props.error?.split('\n'));
    const pdferror = ref<HTMLElement|null>(null);

    function scrollIntoView() {
      let el = pdferror.value?.querySelector('.highlight-error');
      el?.scrollIntoView({behavior: 'auto', block: 'start', inline: 'nearest'});
    }

    onMounted(()=>scrollIntoView());
    onUpdated(()=>scrollIntoView());

    return {
      errmsg,
      pdferror,
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