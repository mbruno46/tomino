import { normalize } from '@tauri-apps/api/path';

// https://manpages.ubuntu.com/manpages/trusty/man5/synctex.5.html

// const unit = Math.pow(2,16);
const unit = 65781.76;
const tag = '(\\d+)'
const link = '(\\d+),(\\d+)(?:,(\\d+))?'
const point = '(-?\\d+),(-?\\d+)'
const size = '(-?\\d+),(-?\\d+),(-?\\d+)'
const width = '(-?\\d+)'
const generic = '((:?.|\\n)*)'

const blockClosures = <{[key:string]:String}>{
  'vbox': ']',
  'hbox': ')',
}

interface blockType {
  [key: string]: [string, RegExp]
}

interface Block {
  'type': String,
  'input': number,
  'line': number,
  'column': number,
  'left': number,
  'bottom': number,
  'width': number,
  'height': number,
  'depth': number,
  'blocks': Block[],
}

// const blocks: blockType = {
//   '[': ['vbox', new RegExp(`\\[${link}:${point}:${size}\\n${generic}`)],
//   '(': ['hbox', new RegExp(`\\(${link}:${point}:${size}\\n${generic}`)],
//   'h': ['void_hbox', new RegExp(`h${link}:${point}:${size}\\n${generic}`)],
//   'v': ['void_vbox', new RegExp(`v${link}:${point}:${size}\\n${generic}`)],
//   'x': ['current', new RegExp(`x${link}:${point}\\n${generic}`)],
//   'k': ['kern', new RegExp(`k${link}:${point}:${width}\\n${generic}`)],
//   'g': ['glue', new RegExp(`g${link}:${point}\\n${generic}`)],
//   '$': ['math', new RegExp(`\\$${link}:${point}\\n${generic}`)],
//   'f': ['ref', new RegExp(`f${tag}:${point}\\n${generic}`)],
//   'r': ['r', new RegExp(`r${link}:${point}:${size}\\n${generic}`)]
// }
const blocks: blockType = {
  '[': ['vbox', new RegExp(`\\[${link}:${point}:${size}`)],
  '(': ['hbox', new RegExp(`\\(${link}:${point}:${size}`)],
  'h': ['void_hbox', new RegExp(`h${link}:${point}:${size}`)],
  'v': ['void_vbox', new RegExp(`v${link}:${point}:${size}`)],
  'x': ['current', new RegExp(`x${link}:${point}`)],
  'k': ['kern', new RegExp(`k${link}:${point}:${width}`)],
  'g': ['glue', new RegExp(`g${link}:${point}`)],
  '$': ['math', new RegExp(`\\$${link}:${point}`)],
  'f': ['ref', new RegExp(`f${tag}:${point}`)],
  'r': ['r', new RegExp(`r${link}:${point}:${size}`)]
}

export function SyncTex() {
  let pages = <{[key: number]: Block}>{};
  let header = {
    version: 0, 
    input: <{[key:string]: string}>{},
    output: '',
    unit: 0,
    magnification: 0,
    xoffset: 0,
    yoffset: 0,
  };

  function parseInput(content: string) {
    for (const i of content.split('\n')) {
      let m = i.match(/^Input:(\d+):(.*)$/);
      if (m) normalize(m[2]).then((data) => header.input[parseInt(m![1])] = data);
    }
  }

  function parseHeader(content: string) {
    let r = [
      'SyncTeX\\sVersion:(\\d+)',
      '(Input:[^]*)',
      'Output:(.*)', 'Magnification:(\\d+)','Unit:(\\d+)',
      'X\\sOffset:(\\d+)','Y\\sOffset:(\\d+)',
      'Content:',
      '([^]*)',
      '(Input:[^]*)','!\\d+','Postamble:','Count:\\d+','!\\d+','Post\\sscriptum:'
    ]
    let m = content.match(new RegExp(r.join('\n')));
    if (m) {
      header['version'] = parseInt(m[1]);
      parseInput(m[2]);
      parseInput(m[9]);
      header['output'] = m[3];
      header['magnification'] = parseInt(m[4]);
      header['unit'] = parseInt(m[5]);
      header['xoffset'] = parseInt(m[6]);
      header['yoffset'] = parseInt(m[7]);
      
      // parse further Inputs in main content and removes them
      let bulk = m[8];
      for (const mm of m[8].match(/Input:.*\n/g) ?? []) {
        parseInput(mm);
        bulk = bulk.replace(mm,'');
      }
      return bulk;
    }
    return '';
  }

  function innerMostBlock(block: Block, x: number, y: number): Block|null {
    let in_block = 0;
    if ((x>=block.left+header.xoffset) && (x<block.left+block.width+header.xoffset)) {in_block++;}
    if ((y<=block.bottom+header.yoffset) && (y>block.bottom-block.height+header.yoffset)) {in_block++;}
    
    let b = null;
    if (in_block==2) {
      let bs = <Block[]>block.blocks;
      b = block;
      for (const _b of bs) {
        let tmp = innerMostBlock(_b, x, y);
        if (tmp) {
          b = tmp;
          break;
        }
      }
    }
    return b;
  }

  function parsePage(content: string) {
    function createBlock(type: string, m: string[], blocks: Block[]) : Block {
      return {
        'type': type,
        'input': parseInt(m[1]),
        'line': parseInt(m[2]),
        'column':  parseInt(m[3] ?? '0'),
        'left': parseInt(m[4]) / unit,
        'bottom': parseInt(m[5]) / unit,
        'width': parseInt(m[6] ?? '0') / unit,
        'height': parseInt(m[7] ?? '0') / unit,
        'depth': parseInt(m[8] ?? '0'),
        'blocks': blocks,
      }
    }

    let lines = content.split('\n');
    let i=0;

    function parseBlock() : Block|null {
      let [type, rex] = blocks[lines[i].substring(0,1)];
      let m = lines[i].match(rex);
      i++;
      if (m==undefined) return null;

      let bs = <Block[]>[];
      if (['vbox','hbox'].includes(type)) {
        while (lines[i].substring(0,1)!=blockClosures[type]) {
          let b = parseBlock();
          if (b) bs.push(b);    
        }
        i++;
      }
      return createBlock(type, m, bs);
    }

    let out = parseBlock();
    if (out==null) console.log('synctex error');
    return out;
  }


  return {
    parse(content: string) {
      let bulk = parseHeader(content);

      let m = <RegExpMatchArray|null>[''];
      for (let id=1;;id++) {
        m = bulk.match(RegExp(`!\\d+\n{${id}\n([^]*)\n!\\d+\n}${id}`));
        if (m) pages[id] = parsePage(m[1])!;
        else break;
      }
    },
    pdf2tex(pageid: number, x: number, y: number) {
      let b = innerMostBlock(pages[pageid], x, y)!;
      return {
        sync: (b) ? true: false,
        path: (b) ? header.input[b.input] : '',
        line: (b) ? b.line: 0,
        column: (b) ? b.column: 0,
      }
    }
  }
}