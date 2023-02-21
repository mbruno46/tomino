<template>
  <div ref="autocomplete" class="autocomplete" :class="(suggestions.length>0) ? '': 'hide'"
    :style="style" contenteditable="false">
    <span v-for="(s, idx) in suggestions" @click="clicked(idx, $event)" :class="(idx==choice) ? 'choice' : ''">{{ s }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, type StyleValue, watchEffect } from 'vue'
import cmds from '@/assets/latex.commands.json';
import envs from '@/assets/latex.environments.json';
import database from '@/helpers/LatexData';

const rcmds = RegExp(/^.*(\\\w+)$/);
const rargs = RegExp(/^.*(\\\w+)(?:\[.*\])?{([^}]*)$/);

function _filter(list: String[], word: string) {
  return list.filter(e => e.replace(/\[?\]?{}/g,'').slice(0,-1).substring(0,word.length)==word)
}

export function Suggestions(text: string): {word: String, suggestions: String[]} {
  if (text.match(rcmds)) {
    let w = text.match(rcmds)![1];
    return {word: w, suggestions: _filter(database.getNewCommands().concat(cmds), w)}
  }
  
  let m = text.match(rargs);
  let out = {word:'', suggestions: <String[]>[]};
  if (m) {
    let c = m[1];
    let w = m[2];
    switch (c) {
      case '\\begin':
      case '\\end':
        out = {word: w, suggestions: _filter(envs, w)};
        break;
      case '\\cite':
        out = {word: w, suggestions: _filter(database.getCites(), w)};
        break;
      case '\\includegraphics':
        out = {word: w, suggestions: _filter(database.getFigures(), w)};
        break;
      default: //includes \ref{}
        out = {word: w, suggestions: _filter(database.getLabels(), w)};
        break;
    }
  }

  return out;
}

let word: String;

export default defineComponent({
  props: {
    input: {
      type: String,
      default: '',
    },
  },
  setup(props) {
    const autocomplete = ref<HTMLElement|null>(null);
    const style = ref<StyleValue>();
    const suggestions = ref<String[]>([]);
    const choice = ref(0);
    
    function setStyle(word: String): StyleValue {
      let parent = autocomplete.value?.parentElement;
      let r0 = parent?.getBoundingClientRect();
      let ofs = parent?.scrollTop ?? 0;
      
      if (document.getSelection()?.rangeCount==0) {return '';}
      let r1 = document.getSelection()?.getRangeAt(0).getClientRects()[0];
      if ((!r1)||(!r0)) {return '';}

      let above = r1.top - r0.top;
      let below = r0.bottom - r1.bottom;
      let max: number = suggestions.value.reduce((max, s) => Math.max(max, s.length), 0);
      let s = `right: max(calc(${r0.right-r1.right}px + ${word.length}ch - ${max}ch), ${0}px);`;

      if (below > above) {
        s += `top: ${r1.bottom - r0.top + ofs}px;`;
        s += `max-height: ${below}px;`
      } else {
        s += `bottom: ${r0.bottom - r1.top - ofs}px;`;
        s += `max-height: ${above}px;`
      }
      return s;
    }

    onMounted(()=>{
      watchEffect(()=>{
        let tmp = Suggestions(props.input);
        suggestions.value = tmp.suggestions;
        choice.value = 0;
        word = tmp.word;
        style.value = setStyle(tmp.word);
      })
    })

    return {
      choice,
      autocomplete,
      style,
      suggestions,
    }
  },
  methods: {
    isActive() {
      return this.suggestions.length>0;
    },
    choose() {
      return this.suggestions[this.choice].substring(word.length);
    },
    clicked(idx: number, event: MouseEvent) {
      this.choice = idx;
      event.stopPropagation();
      event.preventDefault();
      this.autocomplete?.parentElement?.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter'}));
    },
    updown(key: string) {
      if (key=='ArrowUp') this.choice--;
      else if (key=='ArrowDown') this.choice++;
      if (this.choice<0) {this.choice += this.suggestions.length};
      this.choice = this.choice % this.suggestions.length;
    },
  }
});
</script>

<style scoped>
.autocomplete {
  background-color: var(--background);
  width: fit-content;
  border: 2px solid black;
  position: absolute;
  display: flex;
  flex-direction: column;
  overflow-y: scroll;
}

.autocomplete.hide {
  display: none;
}

.autocomplete {
  cursor: pointer;
}

.autocomplete span:hover {
  background-color: var(--background-light);
}

.choice {
  background-color: var(--selection-dark);
  color: var(--text);
}
</style>