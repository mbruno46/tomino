import { readTextFile, exists } from '@tauri-apps/api/fs';
import { extname, join, dirname } from '@tauri-apps/api/path';
import { TimeStamp } from './Utils';

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
  public figures = <string[]>[];

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

  getFigures() {return this.figures}

  getNewCommands() {
    let out = this.newcmds;
    for (const key in this.texfiles) out = out.concat(this.texfiles[key].newcmds);
    return out;
  }
}

class Empty {
  public figures = <string[]>[];

  getLabels() {return []}
  getFigures() {return []}
  getCites() {return []}
  getNewCommands() {return []}
}
export var database: MainTexFile|Empty = new Empty();

export async function initLatexDB(file: string) {
  const ext = await extname(file);
  if (ext!='tex') return;
  database = new MainTexFile(file);
}

export async function addLatexDB(file: string) {
  const ext = await extname(file);
  if (['pdf','jpg','png','jpeg','eps'].includes(ext)) {
    if (!(file in database.figures)) database.figures.push(file);
  }
}