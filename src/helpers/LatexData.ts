import { readTextFile } from '@tauri-apps/api/fs';
import { message } from '@tauri-apps/api/dialog';
import type { FileTree } from './FileTree';
import store from '@/helpers/Store';

const rbib = RegExp(/@\w+{(.*),/);
const rbibg = RegExp(/@\w+{(.*),/g);
const rtex = RegExp(/\\label{(.*)}/);
const rtexg = RegExp(/\\label{(.*)}/g);

function LatexData() {
  let cwd: String;
  let texfiles: {[key:string]: {included:false, labels:String[]}};
  let bibfiles: {[key:string]: {included:false, refs:String[]}};
  let figures:String[];

  function isMain(text: String) {
    return text.match(/^\\documentclass/g);
  }
  
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
        texfiles[name] = {included: false, labels: []};
      }
    } else if (ext=='bib') {
      if (!(name in bibfiles)) {
        bibfiles[name] = {included: false, refs: []};
      }        
    } else if (['pdf','jpg','png','jpeg','eps'].includes(ext)) {
      figures.push(name);
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
      for (const f in texfiles) {
        readTextFile(`${cwd}/${f}`).then((content) => {
          parser(texfiles[f].labels, content, rtexg, rtex);
          if (isMain(content)) {
            if (store.pdf.value.main=='') {
              store.pdf.value.main = f.substring(0,f.lastIndexOf('.'));
              // store.pdf.value.compile = true;
            }
            else message(`Multiple main files detected: ${f}`);
          }
        });
      }
    },
    parseTex(path: string) {
      var key = path.substring(cwd.length+1);
      texfiles[key].labels = [];
      readTextFile(`${cwd}/${key}`).then((content) => {
        parser(texfiles[key].labels, content, rtexg, rtex);
      });
    }
  }
}

var database = LatexData();
export default database;