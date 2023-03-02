<template>
  <div style="background-color: var(--background-dark);">
    <div class="preferences" :style="`height: ${(prefs.visible) ? '40vh' : '0px'}`">
      <div style="font-size: 1.2rem;">
        SETTINGS
      </div>
      <div>
        <label for="checkbox" style="padding: 0 1rem 0 1rem;">latex.synctex</label>
        <input type="checkbox" id="checkbox" v-model="prefs.latex.synctex" />
      </div>
    </div>
    <div class="footer">
      <Loader v-if="loader"></Loader>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref } from 'vue'
import Loader from '@/components/Loader.vue';
import store from '@/helpers/Store'



export default defineComponent({
  components: { Loader },
  setup() {
    const loader = computed(()=>store.pdf.value.loader);
    const prefs = store.Preferences.settings;
    return {
      loader,
      prefs,
    }
  }
});
</script>

<style scoped>
.preferences {
  overflow-y: scroll;
  transition: height 0.5s;
  background-color: var(--background-dark);
  color: var(--text);
}

.preferences div {
  padding: 0.5rem 2rem 0.5rem 2rem;
}

.footer {
  display: flex;
  height: 2rem;
}
</style>