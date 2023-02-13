<template>
  <div ref="code_editor" class="code-editor" @keydown="handleKeyBoard" @mouseup="handleMouseUp">
    <code-line v-for="(val, index) in lines" 
      :key="val" :text="val" :index="index"></code-line>
  </div>
</template>

<script lang="ts">
import CodeLine from './CodeLine.vue';
import { defineComponent, onMounted, onUpdated, ref } from 'vue';
import type { Ref } from 'vue'
import { History, Selection, Caret } from '@/helpers/EditorTools';
import { readTextFile, writeTextFile } from '@tauri-apps/api/fs';
import { writeText, readText } from '@tauri-apps/api/clipboard';

const ntabs = 4;

function Editor() {
  const lines = ref<string[]>([]);

  function forLoop(start: Caret, end: Caret, callback: Function) {
    for (var i=start.idx; i<=end.idx; i++) callback(i);
  }

  return {
    lines,
    init(text: String) {
      lines.value = [];
      lines.value = text.split('\n');
    },
    selectedText(start: Caret, end: Caret) {
      let t = lines.value.slice(start.idx, end.idx+1).join('\n');
      return t.substring(start.pos, t.length + end.pos - lines.value[end.idx].length);
    },
    moveCaret(c: Caret, dir: String) {
      switch (dir) {
        case 'ArrowUp': //moveup
          if (c.idx>0) {
            c.idx--;
            c.pos = (c.pos<lines.value[c.idx].length) ? c.pos : lines.value[c.idx].length;
          }
          break;
        case 'ArrowDown': //movedown
          if (c.idx<lines.value.length-1) {
            c.idx++;
            c.
            pos = (c.pos<lines.value[c.idx].length) ? c.pos : lines.value[c.idx].length;
          }
          break;
        case 'ArrowLeft': //moveleft
          if (c.pos==0) {
            if (c.idx>0) {
              c.idx--;
              c.pos = lines.value[c.idx].length;
            }
          } else c.pos--;
          break;
        case 'ArrowRight': //moveright
          if (c.pos==lines.value[c.idx].length) {
            if (c.idx<lines.value.length-1) {
              c.idx++;
              c.pos = 0;
            }
          } else c.pos++;
          break;
      }
    },
    deleteText(start: Caret, end: Caret) {
      let t0 = lines.value[start.idx].substring(0,start.pos);
      let t1 = lines.value[end.idx].substring(end.pos);
      let t = this.selectedText(start, end);
      lines.value.splice(start.idx, end.idx+1-start.idx, t0 + t1);
      return t;
    },
    insertText(c: Caret, text: String) {
      let ll = text.split('\n');
      let t = lines.value[c.idx].substring(c.pos);
      lines.value[c.idx] = lines.value[c.idx].substring(0,c.pos) + ll[0];
      c.pos += ll[0].length;
      for (var i=1; i<ll.length; i++) {
        c.idx++;
        c.pos = 0;
        lines.value.splice(c.idx, 0, ll[i]);
      }
      lines.value[c.idx] += t;
    },
    newLine(caret: Caret) {
      let t = lines.value[caret.idx].substring(caret.pos);
      lines.value[caret.idx] = lines.value[caret.idx].substring(0,caret.pos);
      lines.value.splice(caret.idx+1, 0, t);
    },
    indent(start: Caret, end: Caret, dir: number) {
      forLoop(start, end, (i: number) => {
        let n = lines.value[i].search(/\S|$/);
        let m = dir + ((dir==1) ? Math.floor(n/ntabs) : Math.ceil(n/ntabs));
        let nt = ntabs*((m<0)? 0:m);
        lines.value[i] = " ".repeat(nt) + lines.value[i].substring(n);
        if (i==start.idx) start.pos += (nt-n);
        if (i==end.idx) end.pos += (nt-n);
      })
      start.pos = (start.pos<0) ? 0 : start.pos;
      end.pos = (end.pos<0) ? 0 : end.pos;
    },
    comment(start: Caret, end: Caret) {
      var count=0;
      forLoop(start, end, (i: number) => {count += (lines.value[i].match(/^\s*%.*$/)) ? 1 : 0;});
      if (count==end.idx+1-start.idx) {
        forLoop(start, end, (i: number) => {
          lines.value[i] = lines.value[i].replace(RegExp(/^(\s*)(%\s?)(.*)$/), function(d,a,b,c) {
            return ((a!='') ? a : '') + ((c!='') ? c : '');
          })
        })
      } else {
        forLoop(start, end, (i: number) => {lines.value[i] = '% ' + lines.value[i]});
      }
    }
  }
}

export default defineComponent({
  components: {CodeLine},
  props: {
    path: String,
  },
  setup(props) {
    const code_editor = ref<HTMLDivElement|null>(null);
    const editor = Editor();
    const s = Selection();
    const lines: Ref<string[]> = editor.lines;
    const history = History(s);

    onMounted(() => {
      if (props.path) {
        readTextFile(props.path).then((content) => {
          editor?.init(content);
        });
      }
    });

    onUpdated(() => {
      if (code_editor.value) s.updateDOM(code_editor.value);
    });

    function deleteSelectedText() {
      let t = '';
      if (!s.anchor.isEqual(s.focus)) {
        if (s.focusIsStart()) {
          t = editor?.deleteText(s.focus, s.anchor);
          s.anchor.copyFrom(s.focus);
        } else {
          t = editor?.deleteText(s.anchor, s.focus);
          s.focus.copyFrom(s.anchor);
        } 
      }
      return t;
    }

    function deleteChar(right: boolean) {
      if (s.anchor.isEqual(s.focus)) editor?.moveCaret(s.focus, (right) ? 'ArrowRight' : 'ArrowLeft')
      return deleteSelectedText();
    }

    function newLine() {
      deleteSelectedText();
      editor?.newLine(s.anchor);
      s.anchor.idx++;
      s.anchor.pos=0;
      s.focus.copyFrom(s.anchor);
    }

    function insertText(text: String) {
      deleteSelectedText();
      editor?.insertText(s.focus,text);
      s.anchor.copyFrom(s.focus);
    }

    function arrows(direction: String, shiftKey: boolean) {
      if (shiftKey) editor.moveCaret(s.focus, direction);
      else {
        if (s.anchor.isEqual(s.focus)) {
          editor.moveCaret(s.focus, direction);
          s.anchor.copyFrom(s.focus);
        }
        else {
          if (['ArrowUp','ArrowDown'].includes(String(direction))) {
            s.anchor.copyFrom(s.focus);
            editor.moveCaret(s.focus, direction);
            s.anchor.copyFrom(s.focus);
          } else {
            if (direction=='ArrowLeft') {
              if (s.focusIsStart()) s.anchor.copyFrom(s.focus)
              else s.focus.copyFrom(s.anchor)
            }
            if (direction=='ArrowRight') {
              if (s.focusIsStart()) s.focus.copyFrom(s.anchor)
              else s.anchor.copyFrom(s.focus);
            }
          }
        }
      }
      if (code_editor.value) s.updateDOM(code_editor.value);
    }

    function indent(rm: boolean) {
      if (s.focusIsStart()) editor?.indent(s.focus, s.anchor, (rm) ? -1:+1);
      else editor?.indent(s.anchor, s.focus, (rm) ? -1:+1);
    }

    function comment() {
      if (s.focusIsStart()) editor?.comment(s.focus, s.anchor);
      else editor?.comment(s.anchor, s.focus);
    }

    function CCP(action: string) {
      if (action=='cut') {
        writeText(deleteSelectedText());
      } else if (action=='copy') {
        let [start, end] = s.getStartEnd();
        writeText(editor.selectedText(start, end));
      } else if (action=='paste') {
        readText().then((data)=>{
          if (data) {
            deleteSelectedText();
            editor?.insertText(s.focus, data);
          }
        });
      }
    }

    function handleMouseUp(event: MouseEvent) {
      s.getFromDOM();
    }

    function saveToDisk() {
      if (props.path) writeTextFile(props.path, editor?.lines.value.join('\n'));
    }

    return {
      code_editor,
      lines,
      newLine,
      insertText,
      deleteChar,
      arrows,
      indent,
      comment,
      handleMouseUp,
      saveToDisk,
      history,
      CCP,
    }
  },
  methods: {
    handleKeyBoard: function(event: KeyboardEvent) {
      this.history.startRecord();

      if ((event.ctrlKey || event.metaKey)) {
        switch (event.key) {
          case 'x':
            this.history.add(()=>{return this.CCP('cut')}, (arg:string)=>{this.insertText(arg)});
            break;
          case 'c':
            this.CCP('copy');
            break;
          case 'v':
            this.history.add(()=>{return this.CCP('paste')}, ()=>{this.CCP('cut')});
            break;
          case 'z':
            (event.shiftKey) ? this.history.forward() : this.history.backward();
            break;
          case '/':
            this.history.add(this.comment, this.comment);
            break;
          case 's':
            this.saveToDisk();
            break;
        }
      }
      else {
        if (event.key.length==1) {
          this.history.add(()=>{this.insertText(event.key)}, ()=>{this.deleteChar(false)})
        } else {
          switch (event.key) {
            case 'ArrowUp':
            case 'ArrowDown':
            case 'ArrowLeft':
            case 'ArrowRight':
              this.arrows(event.key, event.shiftKey);
              break;
            case 'WhiteSpace':
              this.history.add(()=>{this.insertText(" ")}, ()=>{this.deleteChar(false)});
              break;
            case 'Tab':
              this.history.add(()=>{this.indent(event.shiftKey)}, ()=>{this.indent(!event.shiftKey)});
              break;
            case 'Enter':
              this.history.add(this.newLine, ()=>{this.deleteChar(false)});
              break;
            case 'Backspace':
              this.history.add(()=>{return this.deleteChar(false)}, (arg:string)=>{this.insertText(arg)});
              break;
            case 'Delete':
              this.history.add(()=>{return this.deleteChar(true)}, (arg:string)=>{this.insertText(arg)});
              break;
          }
        }
      }

      this.history.endRecord();
      event.preventDefault();
    }
  }
})
</script>

<style scoped>
.code-editor {
  font-family: 'Source Code Pro', monospace;
  display: flex;
  flex-direction: column;
  height: calc(100% - 2rem);
  overflow-y: scroll;
  background: var(--background-light);
  padding-top: 1rem;
  visibility: visible;
  opacity: 1;
  transition: opacity 0.5s, visibility 0.5s;
  position: absolute;
  left: 0;
  right: 0;
}

</style>