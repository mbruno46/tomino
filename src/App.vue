<template>
  <div :class="browser_visible ? '' : 'folded'" class="container">
    <side-bar></side-bar>
    <browser id="browser"></browser>
    <div class="main">
      <editor></editor>
      <viewer></viewer>
    </div>
  </div>
</template>

<script lang="ts">
import Editor from "@/views/Editor.vue";
import Viewer from "@/views/Viewer.vue";
import Browser from "@/views/Browser.vue"
import SideBar from "@/views/SideBar.vue";
import { computed, defineComponent } from 'vue'
import store from '@/helpers/Store'

export default defineComponent({
  components: {
    Editor, Viewer, Browser, SideBar,
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
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 100%;
  overflow: hidden;
}

</style>