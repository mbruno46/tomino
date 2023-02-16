<template>
  <div ref="code_editor" class="code-editor" @keydown="handleKeyBoard" @mouseup="handleMouseUp" contenteditable="true">
    <code-line v-for="(val, index) in lines" 
      :key="val" :text="val" :index="index"></code-line>
    <auto-complete ref="autocomplete" :input="input"></auto-complete>
  </div>
</template>

<script lang="ts">
import CodeLine from './CodeLine.vue';
import { defineComponent, onMounted, onUpdated, ref } from 'vue';
import type { Ref } from 'vue'
import { History, Selection, Caret } from '@/helpers/EditorTools';
import { readTextFile, writeTextFile } from '@tauri-apps/api/fs';
import { writeText, readText } from '@tauri-apps/api/clipboard';

import AutoComplete from './AutoComplete.vue';
import { Suggestions } from '@/helpers/AutoComplete';

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
    textBeforeCaret(c: Caret) {
      return lines.value[c.idx].substring(0,c.pos);
    },
    shiftCaret(c: Caret, shift: number) {
      if (c.pos>=shift) {
        c.pos -= shift;
      } else {
        c.idx--;
        shift -= c.pos+1;
        c.pos = lines.value[c.idx].length;
        this.shiftCaret(c, shift);
      }
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
      for (var i=1; i<ll.length; i++) {
        c.idx++;
        c.pos = 0;
        lines.value.splice(c.idx, 0, ll[i]);
      }
      c.pos += ll[ll.length-1].length;
      lines.value[c.idx] += t;
    },
    newLine(caret: Caret, indent:boolean=false) {
      let t = lines.value[caret.idx].substring(caret.pos);
      lines.value[caret.idx] = lines.value[caret.idx].substring(0,caret.pos);
      let n = lines.value[caret.idx].search(/\S|$/);
      let m = Math.floor(n/ntabs)+(indent ? 1: 0);
      console.log(n,m,lines.value[caret.idx]);
      lines.value.splice(caret.idx+1, 0, " ".repeat(m*ntabs) + t);
      return m*ntabs;
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
  components: {
    CodeLine, AutoComplete,
  },
  props: {
    path: String,
  },
  setup(props) {
    const code_editor = ref<HTMLDivElement|null>(null);
    const editor = Editor();
    const s = Selection();
    const lines: Ref<string[]> = editor.lines;
    const history = History(s);
    const input = ref('');
    const autocomplete = ref<typeof AutoComplete|null>(null);

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

    function _deleteSelectedText() {
      let t = '';
      if (!s.anchor.isEqual(s.focus)) {
        let [start, end] = s.getStartEnd();
        t = editor?.deleteText(start, end);
        if (s.focusIsStart()) {
          s.anchor.copyFrom(s.focus);
        } else {
          s.focus.copyFrom(s.anchor);
        } 
      }
      console.log('dddd',s);
      return t;
    }

    function _insertText(text: String) {
      if (text=="") {return}
      editor?.insertText(s.focus, text);
    }

    function _collapse() {
      s.anchor.copyFrom(s.focus);
    }

    function deleteSelectedText() {
      history.add(
        ()=>{return _deleteSelectedText()},
        (arg:string)=>{_insertText(arg)}
      )
      history.stop();
    }

    function deleteChar(right: boolean) {
      history.add(
        ()=>{
          if (s.anchor.isEqual(s.focus)) editor?.moveCaret(s.focus, (right) ? 'ArrowRight' : 'ArrowLeft')
          return _deleteSelectedText();
        },
        (arg:String)=>{_insertText(arg); _collapse();}
      )
      history.stop();
    }

    function newLine() {
      history.add(
        ()=>{return _deleteSelectedText()},
        (arg:string)=>{_insertText(arg)}
      )
      history.add(
        ()=>{
          let n = editor?.newLine(s.anchor); 
          s.anchor.idx++;
          s.anchor.pos=n;
          s.focus.copyFrom(s.anchor);
          return n;
        },
        (n:number)=>{editor?.shiftCaret(s.focus, n+1); _deleteSelectedText();},
      )
      history.stop();
    }

    function insertText(text: String) {
      history.add(
        ()=>{return _deleteSelectedText()},
        (arg:string)=>{_insertText(arg)}
      )
      history.add(
        ()=>{_insertText(text); _collapse();},
        ()=>{editor?.shiftCaret(s.anchor, text.length); _deleteSelectedText()}
      );
      history.stop();
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

    function _indent(rm: boolean) {
      let [start, end] = s.getStartEnd();
      editor?.indent(start, end, (rm) ? -1:+1);
    }

    function indent(rm: boolean) {
      history.add(()=>{_indent(rm)},()=>{_indent(!rm)})
      history.stop();
    }

    function _comment() {
      let [start, end] = s.getStartEnd();
      editor?.comment(start, end);
    }

    function comment() {
      history.add(()=>{_comment()},()=>{_comment()});
      history.stop();
    }

    async function clipboard(read: boolean): Promise<string|null> {
      if (read) {
        const text = await readText();
        return text;
      } else {
        let [start, end] = s.getStartEnd();
        writeText(editor.selectedText(start, end));
      }
      return null;      
    } 


    return {
      code_editor,
      lines,
      input,
      autocomplete,
      newLine,
      insertText,
      deleteChar,
      deleteSelectedText,
      arrows,
      indent,
      comment,
      clipboard,
      undo() {history.backward();},
      redo() {history.forward();},
      handleMouseUp(event: MouseEvent) {
        if (!(autocomplete?.value?.isActive())) s.getFromDOM();
      },
      saveToDisk() {
        if (props.path) writeTextFile(props.path, editor?.lines.value.join('\n'));
      },
      textBeforeCaret() {
        return (editor) ? editor.textBeforeCaret(s.focus) : '';
      },
      autoComplete(word: String) {
        insertText(word);
        let n = word.replace(/\\?\w+/,'').length;
        if (n>0) {
          editor?.shiftCaret(s.focus, n-1);
          _collapse();
        }
      }
    }
  },
  methods: {
    handleKeyBoard: async function(event: KeyboardEvent) {
      if ((event.ctrlKey || event.metaKey)) {
        switch (event.key) {
          case 'x':
            this.clipboard(false);
            this.deleteSelectedText();
            break;
          case 'c':
            this.clipboard(false);
            break;
          case 'v':
            this.clipboard(true).then((t) => {
              if (t) this.insertText(t);
            });
            break;
          case 'z':
            (event.shiftKey) ? this.redo() : this.undo();
            break;
          case '/':
            this.comment();
            break;
          case 's':
            this.saveToDisk();
            break;
        }
      }
      else {
        if (event.key.length==1) {
          this.insertText(event.key);
        } else {
          switch (event.key) {
            case 'ArrowUp':
            case 'ArrowDown':
              if (this.autocomplete?.isActive()) this.autocomplete?.updown(event.key);
              else this.arrows(event.key, event.shiftKey);
              break;
            case 'ArrowLeft':
            case 'ArrowRight':
              this.arrows(event.key, event.shiftKey);
              break;
            case 'WhiteSpace':
              this.insertText(" ");
              break;
            case 'Tab':
              this.indent(event.shiftKey);
              break;
            case 'Enter':
              if (this.autocomplete?.isActive()) this.autoComplete(this.autocomplete?.choose());
              else this.newLine();
              break;
            case 'Backspace':
              this.deleteChar(false);
              break;
            case 'Delete':
              this.deleteChar(true);
              break;
          }
        }
      }

      event.preventDefault();

      // wait for DOM to update
      await this.$nextTick();
      this.input = this.textBeforeCaret();
    }
  }
})
</script>

<style scoped>
.code-editor {
  font-family: 'Source Code Pro', monospace;
  display: flex;
  flex-direction: column;
  height: calc(100% - 4rem);
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