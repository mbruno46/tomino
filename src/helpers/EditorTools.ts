// import { debounce } from "./Utils";

export class Caret {
  idx: number;
  pos: number;

  constructor(idx: number=0, pos: number=0) {
    this.idx = idx;
    this.pos = pos;
  }

  isEqual(c: Caret) {
    return (this.idx == c.idx)&&(this.pos==c.pos)
  }
  isGreater(c: Caret) {
    if (this.idx==c.idx) {
      return (this.pos > c.pos);
    }
    return this.idx > c.idx;
  }
  copyFrom(c: Caret) {
    this.idx = c.idx;
    this.pos = c.pos;
  }
  shift(shift: number, lines: Array<String>) {
    while (shift>0) {
      if (shift > lines[this.idx].length) {
        this.idx++;
        this.pos = 0;
        shift -= lines[this.idx].length;
      } else {
        this.pos += shift;
        shift = 0;
      }
    }
  }
}

export function Selection() {
  var anchor = new Caret;
  var focus = new Caret;

  function getNodeOffset(node: Node, pos: number): [Node|null, number] {
    if (pos==0) {return [node, 0]}
    
    if (node.hasChildNodes()) {
      for (const child of node.childNodes) {
        let tmp = getNodeOffset(child, pos);
        // console.log(node, child, tmp);
        if (tmp[0]!=null) {
          node = tmp[0];
          pos = tmp[1];
          return tmp;
        }
        else {pos = tmp[1]}
      }
      return [null, pos];
    } else {
      if (!node.textContent) {return [null, pos]}
      if (pos > node.textContent.length) {
        return [null, pos-node.textContent?.length]
      }
    }
    return [node, pos]
  }

  function getDivLine(node: Node): [HTMLElement, number] {
    if (node.nodeType == node.ELEMENT_NODE) {
      let el = node as HTMLElement;
      if (el.hasAttribute("linenumber")) {
        let idx = el.getAttribute('linenumber');
        return [el, parseInt(idx ? idx : '0')]
      }
    }
    return getDivLine(node.parentNode as Node);
  }

  function getLength(el: HTMLElement, n: Node, ofs: number) {
    let r = new Range();
    r.selectNodeContents(el);
    r.setEnd(n, ofs);
    return r.toString().length;
  }

  return {
    anchor,
    focus,
    focusIsStart() {return this.anchor.isGreater(this.focus)},
    getStartEnd() {
      if (this.anchor.isGreater(this.focus)) return [this.focus, this.anchor];
      return [this.anchor, this.focus];
    },
    getRange(parent: HTMLElement) {
      let r = document.createRange();
      let el: Element, c: Node|null, o: number;
      let [start, end] = this.getStartEnd();

      el = parent.querySelector(`[linenumber="${start.idx}"]`)!;
      [c, o] = getNodeOffset(el, start.pos);
      console.log(start, c, o, el);
      r.setStart(c!, o);

      el = parent.querySelector(`[linenumber="${end.idx}"]`)!;
      [c, o] = getNodeOffset(el, end.pos);
      r.setEnd(c!, o);    

      return r;
    },
    updateDOM(parent: HTMLElement) {
      let el = parent.querySelector(`[linenumber="${this.focus.idx}"]`);
      el?.scrollIntoView({behavior: 'auto', block: 'nearest', inline: 'nearest'});

      var sel = document.getSelection();
      sel?.removeAllRanges();
      sel?.addRange(this.getRange(parent))
    },
    getFromDOM() {
      var s = document.getSelection();
      if ((s != null) && (s.anchorNode) && (s.focusNode)) {
        console.log(getDivLine(s.anchorNode));

        let [el, idx] = getDivLine(s.anchorNode);
        this.anchor.idx = idx;
        this.anchor.pos = getLength(el, s.anchorNode, s.anchorOffset);

        [el, idx] = getDivLine(s.focusNode);
        this.focus.idx = idx;
        this.focus.pos = getLength(el, s.focusNode, s.focusOffset);
      }
    },
  }
}


export function History(sel: any) {
  interface Record {
    anchor: Caret
    focus: Caret
    action: Function
  }
  interface Stack {
    undo: Record[];
    redo: Record[];
  } 

  let stack:Stack[] = [];
  let stack_undo:Record[] = [];
  let stack_redo:Record[] = [];
  let idx = 0;
  let max = 10;
  let composing = false; 
  let timer = 0;

  function reset() {
    if(stack_redo.length != stack_undo.length) {console.log('error')}

    if (stack_redo.length>0) {
      stack.splice(idx, max-idx, {undo: stack_undo, redo: stack_redo});
      idx++;
      if (idx==max) {
        stack.splice(0,1);
        idx--;
      }
    }

    stack_undo = [];
    stack_redo = [];
  }

  return {
    stack,
    stop() {
      if (!composing) {return}
      reset();
    },
    add(action: Function, reverse: Function) {
      if (!composing) {
        composing = true;
      }

      stack_redo.push({
        anchor: new Caret(sel.anchor.idx, sel.anchor.pos),
        focus: new Caret(sel.focus.idx, sel.focus.pos),
        action: action,
      });

      let out = action();
      // console.log('qua qua ', out);

      stack_undo.push({
        anchor: new Caret(sel.anchor.idx, sel.anchor.pos),
        focus: new Caret(sel.focus.idx, sel.focus.pos),
        action: (out!=undefined) ? ()=>{reverse(out)} : reverse,
      });
    },
    backward() {
      if (idx==0) {return;}
      idx--;
      console.log(idx, stack, stack[idx]);

      for (const s of stack[idx].undo.reverse()) {
        sel.anchor.copyFrom(s.anchor);
        sel.focus.copyFrom(s.focus);
        s.action();        
      }
    },
    forward() {
      if ((idx==max)||(idx==stack.length)) {return;}

      for (const s of stack[idx].redo) {
        sel.anchor.copyFrom(s.anchor);
        sel.focus.copyFrom(s.focus);
        s.action();        
      }
      idx++;
    },
  }
}

export default {
  Caret,
  Selection,
  History,
}