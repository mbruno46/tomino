<template>
  <div class="nav-label">
    <iconify :tag="(icon!='') ? icon : name"></iconify>
    <span :class="(ismain) ? 'main' : ''">{{ name }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Iconify from './Iconify.vue';

export default defineComponent({
  components: { Iconify },
  props: {
    name: String,
    icon: {type: String, default: ''},
    ismain: Boolean,
  },
  // setup() {    
  // },
});
</script>

<style scoped>
.nav-label {
  padding-top: 0.2rem;
  padding-bottom: 0.2rem;
  /* display: grid; */
  /* grid-template-columns: min-content min-content; */
  display: inline-flex;
  /* vertical-align: middle; */
  /* line-height: 1; */
}

.nav-label span {
  display: inline-flex;
  align-items: center;
  padding-left: 0.4rem;
  padding-right: 0.4rem;
}

.main {
  text-decoration: underline;
}
</style>