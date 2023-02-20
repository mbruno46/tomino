<template>
  <div class="footer">
    <Loader v-if="loader"></Loader>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'
import Loader from '@/components/Loader.vue';
import store from '@/helpers/Store'

export default defineComponent({
  components: { Loader },
  setup() {
    const loader = computed(()=>store.pdf.value.loader);
    return {
      loader,
    }
  }
});
</script>

<style scoped>
.footer {
  display: flex;
  height: 2rem;
  background-color: var(--background-dark);
}
</style>