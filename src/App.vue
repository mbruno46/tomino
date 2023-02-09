<template>
  <div :class="browser_visible ? '' : 'folded'" class="container">
    <tool-bar></tool-bar>
    <browser id="browser"></browser>
    <div class="main">
      <editor></editor>
    </div>
  </div>
</template>

<script lang="ts">
import Editor from "./components/Editor.vue";
import Browser from "./components/Browser.vue"
import ToolBar from "./components/ToolBar.vue";
import { computed, defineComponent } from 'vue'
import store from '@/helpers/Store'

export default defineComponent({
  components: {
    Editor, Browser, ToolBar,
  },
  setup() {
    const browser_visible = computed(() => store.browser.value.visible);

    return {
      browser_visible,
    }
  },
})
</script>

<style scoped>
.container {
  height: 100vh;
  width: 100vw;
  display: grid;
  grid-template-columns: 3rem auto 1fr;
}
.container #browser {
  width: 16rem;
}
.container.folded #browser {
  width: 0px;
}

#browser {
  transition: width 0.5s ease;
  height: 100%;
}

.main {
  height: 100%;
}

</style>