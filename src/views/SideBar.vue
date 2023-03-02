<template>
  <div class="toolbar">
    <icon-button :tag="browser_visible ? 'left-fill' : 'files'" @click="browserVisibility" :fontsize="2"></icon-button>
    <icon-button :tag="'refresh'" :fontsize="2" @click="recompile"></icon-button>
    <icon-button :tag="'settings'" :fontsize="2" style="position: absolute; bottom: 0"
      @click="preferences"></icon-button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import IconButton from '@/components/IconButton.vue';
import store from '@/helpers/Store';

export default defineComponent({
  components: {
    IconButton,
  },
  emits: ['toggleBrowser'],
  setup() {
    const browser_visible = ref(true);
    return {
      browser_visible,
    }
  },
  methods: {
    browserVisibility() {
      this.$emit('toggleBrowser');
      this.browser_visible = !this.browser_visible;
    },
    recompile() {
      store.pdf.value.compile = 2;
    },
    preferences() {
      store.Preferences.settings.value.visible = !store.Preferences.get('visible');
    }
  }
})
</script>

<style scoped>
.toolbar {
  display: flex;
  flex-flow: column;
  height: 100%;
  background-color: var(--background-dark);
  position: relative;
}

</style>