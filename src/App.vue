<template>
  <div :class="browser_visible ? '' : 'folded'" class="container">
    <side-bar @toggle-browser="browser_visible = !browser_visible"></side-bar>
    <browser id="browser"></browser>
    <div ref="main" class="main" @mousemove="mousemove" @mouseup="mouseup">
      <editor ></editor>
      <div class="draggable" @mousedown="mousedown"></div>
      <viewer></viewer>
    </div>
    <Footer id="footer"></Footer>
  </div>
</template>

<script lang="ts">
import Editor from "@/views/Editor.vue";
import Viewer from "@/views/Viewer.vue";
import Browser from "@/views/Browser.vue"
import SideBar from "@/views/SideBar.vue";
import Footer from "./views/Footer.vue";
import { defineComponent, onMounted, ref } from 'vue'

function Resizer() {
  let origin = 0;
  let active = false; 
  let width = 0;
  let parent: HTMLElement;

  return {
    init(p: HTMLElement) {
      parent = p;
      width = Math.floor(p.clientWidth/2-2);
    },
    start(event: MouseEvent) {
      active = true;
      origin = event.x;
    },
    move(event: MouseEvent) {
      if (active) parent.style.gridTemplateColumns = `minmax(8rem,${width + (event.x-origin)}px) 4px minmax(11rem,1fr)`;
    },
    end(event: MouseEvent) {
      this.move(event);
      active = false;
    }
  }
}

export default defineComponent({
  components: {
    Editor, Viewer, Browser, SideBar, Footer,
  },
  setup() {
    const browser_visible = ref(true);
    let r = Resizer();
    const main = ref<HTMLElement|null>(null);

    onMounted(()=>{
      if (main.value) r.init(main.value);
    });

    return {
      main,
      browser_visible,
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
</style>