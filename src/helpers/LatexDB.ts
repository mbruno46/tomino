import { ref } from 'vue';
import { readDir, readTextFile, exists } from '@tauri-apps/api/fs';
import { extname, join, dirname , basename} from '@tauri-apps/api/path';
import { TimeStamp } from './Utils';
import store from './Store';

const rbib = RegExp(/@\w+{(.*),/);
const rbibg = RegExp(/@\w+{(.*),/g);
const rtex = RegExp(/\\label{(.*)}/);
const rtexg = RegExp(/\\label{(.*)}/g);
const rnewcmd = RegExp(/\\newcommand{(.*)}(\[.*\])?{.*}/);
const rnewcmdg = RegExp(/\\newcommand{(.*)}(\[.*\])?{.*}/g);
const rdef = RegExp(/\\def(\s?\\\w+)/);
const rdefg = RegExp(/\\def(\s?\\\w+)/g);


function parser(text: String, rexg: RegExp, rex: RegExp): String[] {
  let arr: String[] = [];
  text.match(rexg)?.forEach((m) => {
    let _m = m.match(rex);
    if (_m) arr.push(_m[1]);
  });
  return arr;
}

class File {
  path: string;
  timestamp: number = 0;

  constructor(p: string) {
    this.path = p;
    this.update();
    
    TimeStamp(this.path, (t:number)=>{this.timestamp=t});
    setInterval(()=>TimeStamp(this.path, (t:number)=>{
      if (t>this.timestamp) {
        this.update();
        this.timestamp = t;
      }
    }), 2000);
  }

  async update() {}
}

class TexFile extends File {
  labels: String[] = [];
  newcmds: String[] = [];

  async update() {
    const content = await readTextFile(this.path);
    this.labels = parser(content, rtexg, rtex)
    this.newcmds = parser(content, rnewcmdg, rnewcmd).concat(parser(content, rdefg, rdef));  
  }
}

class BibFile extends File {
  included: boolean = false;
  refs: String[] = [];

  async update() {
    const content = await readTextFile(this.path);
    this.refs = parser(content, rbibg, rbib);
  }
}

class MainTexFile extends TexFile {
  texfiles = <{[key:string]: TexFile}>{};
  bibfiles = <{[key:string]: BibFile}>{};

  async bibliography(content: string, cwd: string) {
    let include = [];

    let mm = content.match(/\\bibliography{.*}/g);
    if (mm) {
      for (const m of mm) {
        let fname = m.replace(/\\bibliography{(.*)}/,'$1').replace(/(.*)(.bib)?/,'$1.bib');
        const path = await join(cwd, fname);
        if (!(await exists(path))) continue;
        include.push(path);
        if (!(path in this.bibfiles)) this.bibfiles[path] = new BibFile(path);
      }
    }

    for (const key in this.bibfiles) {
      if (!include.includes(key)) delete this.bibfiles[key];
    }
  }

  async include(content: string, cwd: string) {
    let include = [this.path];

    let mm = content.match(/\\input{.*}/g);
    if (mm) {
      for (const m of mm) {
        let fname = m.replace(/\\input{(.*)}/,'$1').replace(/(.*)(.tex)?/,'$1.tex');
        const path = await join(cwd, fname);
        if (!(await exists(path))) continue;
        include.push(path);
        if (!(path in this.texfiles)) this.texfiles[path] = new TexFile(path);
      }
    }

    mm = content.match(/\\include{.*}/g);
    if (mm) {
      for (const m of mm) {
        let fname = m.replace(/\\include{(.*)}/,'$1').replace(/(.*)(.tex)?/,'$1.tex');
        const path = await join(cwd, fname);
        if (!(await exists(path))) continue;
        include.push(path);
        if (!(path in this.texfiles)) this.texfiles[path] = new TexFile(path);
      }
    }

    for (const key in this.texfiles) {
      if (!include.includes(key)) delete this.texfiles[key];
    }
  }

  async update() {
    let content = await readTextFile(this.path);
    this.labels = parser(content, rtexg, rtex)
    this.newcmds = parser(content, rnewcmdg, rnewcmd).concat(parser(content, rdefg, rdef));  

    const cwd = await dirname(this.path);
    await this.bibliography(content, cwd);
    this.include(content, cwd);
    console.log(this);
  }

  getLabels() {
    let out = this.labels;
    for (const key in this.texfiles) out = out.concat(this.texfiles[key].labels);
    return out;      
  }

  getCites() {
    let out = <String[]>[];
    for (const key in this.bibfiles) out = out.concat(this.bibfiles[key].refs);
    console.log(this)
    return out;      
  }
  
  getNewCommands() {
    let out = this.newcmds;
    for (const key in this.texfiles) out = out.concat(this.texfiles[key].newcmds);
    return out;
  }
}

class Empty {
  getLabels() {return []}
  getCites() {return []}
  getNewCommands() {return []}
}
export var database: MainTexFile|Empty = new Empty();

export async function initLatexDB(file: string) {
  const ext = await extname(file);
  if (ext!='tex') return;
  database = new MainTexFile(file);
  const name = await basename(file);
  store.pdf.value.main = name.substring(0, name.length - 4);
}

function FileSystem() {
  let path: string;
  let texfiles = <string[]>[];
  let bibfiles = <string[]>[];
  let figures = <string[]>[];
  let files = <string[]>[];

  function arrayFromType(p: string): string[] {
    var ext = p.substring(p.lastIndexOf('.')+1);
    if (ext=='tex') return texfiles;
    else if (ext=='bib') return bibfiles;
    else if (['pdf','jpg','png','jpeg','eps'].includes(ext)) return figures;
    return files;
  }

  return {
    texfiles,
    bibfiles,
    figures,
    files,
    init(p: string) {
      path = p;
    },
    add(p: string) {
      let arr = arrayFromType(p);
      var name = p.substring(path.length+1);
      if (!arr.includes(p)) arr.push(name)
    },
    rm(p: string) {
      let arr = arrayFromType(p);
      var name = p.substring(path.length+1);
      if (arr.includes(name)) arr.splice(arr.indexOf(name), 1)
    }
  }
}

export var fs = FileSystem();

export function Folder() {
  let path: string = '';
  let timestamp: number = 0;
  let subfolders = ref<string[]>([]);
  let files = ref<string[]>([]);
  
  async function update() {
    readDir(path, {recursive: false}).then((entries)=>{
      let keep = <string[]>[]

      for (const c of entries) {
        if (!c.name) continue;
        if (c.name?.substring(0,1)=='.') continue;

        if (c.children) {
          if (!(subfolders.value.includes(c.path))) subfolders.value.push(c.path);
        } else {
          if (!(files.value.includes(c.path))) files.value.push(c.path);
          fs.add(c.path);
        }

        keep.push(c.path);
      }

      // clean
      const clean = (arr: string[], isfile: boolean) => {
        for (var i of arr) if (!keep.includes(i)) {
          arr.splice(arr.indexOf(i),1);
          if (isfile) fs.rm(i);
        }
      }
      clean(files.value, true);
      clean(subfolders.value, false);

      files.value.sort();
      subfolders.value.sort();
    });
  }

  return {
    subfolders,
    files,
    init(p: string) {
      path = p;
      update();
      
      TimeStamp(path, (t:number)=>{timestamp=t});
      setInterval(()=>TimeStamp(path, (t:number)=>{
        if (t>timestamp) {
          update();
          timestamp = t;
        }
      }), 2000);
    }
  }
}
