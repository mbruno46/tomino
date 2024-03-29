<template>
  <div :class="browser_visible ? '' : 'folded'" class="container">
    <side-bar @toggle-browser="browser_visible = !browser_visible"></side-bar>
    <browser id="browser"></browser>
    <div ref="main" class="main" @mousemove="mousemove" @mouseup="mouseup">
      <editor></editor>
      <div class="draggable" @mousedown="mousedown"></div>
      <viewer></viewer>
    </div>
    <Footer id="footer"></Footer>
  </div>
  <splash></splash>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'

import Editor from "@/views/Editor.vue";
import Viewer from "@/views/Viewer.vue";
import Browser from "@/views/Browser.vue"
import SideBar from "@/views/SideBar.vue";
import Footer from "./views/Footer.vue";
import Splash from "./views/Splash.vue";

function Resizer() {
  let origin = 0;
  let active = false; 
  let width = 0;
  let parent: HTMLElement;

  return {
    init(p: HTMLElement) {
      parent = p;
    },
    start(event: MouseEvent) {
      active = true;
      origin = event.x;
      width = parent.children[0].clientWidth;
      event.stopPropagation();
    },
    move(event: MouseEvent) {
      let percent = (width + event.x-origin) / parent.clientWidth * 100;
      if (active) parent.style.gridTemplateColumns = `minmax(8rem,${percent}%) 4px minmax(11rem,1fr)`;
      event.stopPropagation();
    },
    end(event: MouseEvent) {
      this.move(event);
      active = false;
      event.stopPropagation();
    }
  }
}

export default defineComponent({
  components: {
    Editor,
    Viewer,
    Browser,
    SideBar,
    Footer,
    Splash
},
  setup() {
    const browser_visible = ref(true);
    let r = Resizer();
    const main = ref<HTMLElement|null>(null);
    const prefs = ref(false);

    onMounted(()=>{
      if (main.value) r.init(main.value);
    });

    return {
      main,
      browser_visible,
      prefs,
      mousedown(event: MouseEvent) {r.start(event)},
      mousemove(event: MouseEvent) {r.move(event)},
      mouseup(event: MouseEvent) {r.end(event)},
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
  grid-template-columns: 1fr 4px 1fr;
  height: 100%;
  overflow: hidden;
}

.main .draggable {
  height: 100%;
  background-color: var(--background-dark);
  cursor: col-resize;
}

#footer {
  grid-area: footer;
}

@font-face{
    font-family: 'Source Code Pro';
    font-weight: 200;
    font-style: normal;
    font-stretch: normal;
    src: url('@/assets/source-code-pro/SourceCodePro-Regular.ttf') format('truetype');
}
</style>