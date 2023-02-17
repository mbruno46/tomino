<template>
  <div :class="browser_visible ? '' : 'folded'" class="container">
    <side-bar @toggle-browser="browser_visible = !browser_visible"></side-bar>
    <browser id="browser"></browser>
    <div class="main">
      <editor></editor>
      <viewer></viewer>
    </div>
    <bottom-bar id="footer"></bottom-bar>
  </div>
</template>

<script lang="ts">
import Editor from "@/views/Editor.vue";
import Viewer from "@/views/Viewer.vue";
import Browser from "@/views/Browser.vue"
import SideBar from "@/views/SideBar.vue";
import BottomBar from "./views/BottomBar.vue";
import { defineComponent, ref } from 'vue'

export default defineComponent({
  components: {
    Editor, Viewer, Browser, SideBar, BottomBar,
  },
  setup() {
    const browser_visible = ref(true);
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
  grid-template-columns: auto auto 1fr;
  grid-template-rows: 1fr min-content;
  grid-template-areas: "sidebar browser main" 
    "footer footer footer";
}
.container #browser {
  width: 16rem;
}
.container.folded #browser {
  width: 0px;
}

#browser {
  grid-area: browser;
  transition: width 0.5s ease;
  /* height: 100%; */
}

.main {
  grid-area: main;
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 100%;
  overflow: hidden;
}

#footer {
  grid-area: footer;
}
</style>