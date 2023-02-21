import { readTextFile } from '@tauri-apps/api/fs';
import { message } from '@tauri-apps/api/dialog';
import type { FileTree } from './FileTree';
import store from '@/helpers/Store';

const rbib = RegExp(/@\w+{(.*),/);
const rbibg = RegExp(/@\w+{(.*),/g);
const rtex = RegExp(/\\label{(.*)}/);
const rtexg = RegExp(/\\label{(.*)}/g);
const rnewcmd = RegExp(/\\newcommand{(.*)}(\[.*\])?{.*}/);
const rnewcmdg = RegExp(/\\newcommand{(.*)}(\[.*\])?{.*}/g);
const rdef = RegExp(/\\def(\s?\\\w+)/);
const rdefg = RegExp(/\\def(\s?\\\w+)/g);

function LatexData() {
  let cwd: String;
  let texfiles: {[key:string]: {included:boolean, labels:String[], newcmds: String[]}};
  let bibfiles: {[key:string]: {included:boolean, refs:String[]}};
  let figures:String[];
  
  async function parser(arr: String[], text: String, rexg: RegExp, rex: RegExp) {
    text.match(rexg)?.forEach((m) => {
      let _m = m.match(rex);
      if (_m) arr.push(_m[1]);
    })
  }

  function init(rootdir: String) {
    cwd = rootdir;
    store.pdf.value.main = '';
    figures = [];
    texfiles = {};
    bibfiles = {};
  }

  function addFile(path: string) {
    var ext = path.substring(path.lastIndexOf('.')+1);
    var name = path.substring(cwd.length+1);
    if (ext=='tex') {
      if (!(name in texfiles)) {
        texfiles[name] = {included: false, labels: [], newcmds: []};
      }
    } else if (ext=='bib') {
      if (!(name in bibfiles)) {
        bibfiles[name] = {included: false, refs: []};
      }        
    } else if (['pdf','jpg','png','jpeg','eps'].includes(ext)) {
      figures.push(name);
    }
  }

  async function parseMain(maintex: string) {
    let content = await readTextFile(`${cwd}/${maintex}`);
    let mm = content.match(/\\bibliography{.*}/g);
    if (mm) {
      for (const m of mm) {
        let fname = m.replace(/\\bibliography{(.*)}/,'$1').replace(/(.*)(.bib)?/,'$1.bib');
        if (fname in bibfiles) {
          bibfiles[fname].included = true;
        }
      }
    }

    mm = content.match(/\\input{.*}/g);
    if (mm) {
      for (const m of mm) {
        let fname = m.replace(/\\input{(.*)}/,'$1').replace(/(.*)(.tex)?/,'$1.tex');
        if (fname in bibfiles) {
          texfiles[fname].included = true;
        }
      }
    }

    mm = content.match(/\\include{.*}/g);
    if (mm) {
      for (const m of mm) {
        let fname = m.replace(/\\include{(.*)}/,'$1').replace(/(.*)(.tex)?/,'$1.tex');
        if (fname in bibfiles) {
          texfiles[fname].included = true;
        }
      }
    } 
  }

  return {
    importFromFileTree(input: FileTree) {
      function inner(input: FileTree) {
        for (const f of input.files) addFile(f.path);
        for (const f of input.subfolders) inner(f);  
      }
      init(input.path);
      inner(input);

      for (const f in bibfiles) {
        readTextFile(`${cwd}/${f}`).then((content) => {
          parser(bibfiles[f].refs, content, rbibg, rbib);
        })
      }
      for (const f in texfiles) this.parseTex(`${cwd}/${f}`);
    },
    setMain(fname: string) {
      if (fname.includes('/')) {
        message('Main tex file should be in project root directory');
        return
      }
      if (!(fname in texfiles)) {
        message(`Cannot set ${fname} as main tex file`);
        return;
      }
      store.pdf.value.main = fname.substring(0,fname.lastIndexOf('.'));
      for (const key in texfiles) texfiles[key].included = false;
      texfiles[fname].included = true;
      parseMain(fname);
      // store.pdf.value.compile = true;
    },
    parseTex(path: string) {
      var key = path.substring(cwd.length+1);
      texfiles[key].labels = [];
      texfiles[key].newcmds = [];
      readTextFile(`${cwd}/${key}`).then((content) => {
        parser(texfiles[key].labels, content, rtexg, rtex);
        parser(texfiles[key].newcmds, content, rnewcmdg, rnewcmd);
        parser(texfiles[key].newcmds, content, rdefg, rdef);
        
        for (const l of content.split('\n')) {
          if (l.match(/\s*\\documentclass/)) {
            if (store.pdf.value.main=='') this.setMain(key);
            else message(`Multiple main files detected: ${key}`);
          } 
        }
      });
    },
    getLabels() {
      let out = <String[]>[];
      for (const key in texfiles) {
        if (texfiles[key].included) out = out.concat(texfiles[key].labels);
      }
      return out;
    },
    getNewCommands() {
      let out = <String[]>[];
      for (const key in texfiles) {
        if (texfiles[key].included) out = out.concat(texfiles[key].newcmds);
      }
      return out;
    },
    getCites() {
      let out = <String[]>[];
      for (const key in bibfiles) {
        if (bibfiles[key].included) out = out.concat(bibfiles[key].refs);
      }
      return out;      
    },
    getFigures() {return figures;}
  }
}

var database = LatexData();
export default database;