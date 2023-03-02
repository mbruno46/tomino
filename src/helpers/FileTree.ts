import type { FileEntry } from '@tauri-apps/api/fs';

export class FileTree {
  path: string;
  name: string;
  files: FileTree[];
  subfolders: FileTree[];

  constructor(path: string='', name: string|undefined=undefined, children: FileEntry[]|undefined=undefined) {
    this.path = path;
    this.name = name ? name : '?';
    this.files = [];
    this.subfolders = [];
    if (children) {
      for (const c of children) {
        if (c.name?.substring(0,1)=='.') continue;
        
        if (c.children) {
          this.subfolders.push(new FileTree(c.path, c.name, c.children));
        } else {
          this.files.push(new FileTree(c.path, c.name, undefined));
        }
      }
    }
  }
}