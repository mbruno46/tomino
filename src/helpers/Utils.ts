import { listen } from '@tauri-apps/api/event';
import { invoke } from '@tauri-apps/api/tauri';
import { Command } from '@tauri-apps/api/shell';

export function wrapper(name:string, f: Function) {
  (async ()=> {
    const out = await listen(name, ()=>{f()});
  })();
}

export function CreateProject(path: string) {
  invoke('create_project', {path: path});
}

export function FileWatcher(callback: Function) {
  let time: number;
  let skip = false;
  let timer: number; 

  return {
    init(path: string) {
      invoke<number>('timestamp',{ path: path }).then((t)=>time=t);

      timer = setInterval(() => {
        invoke<number>('timestamp',{ path: path }).then((t)=>{
          if (t>time) {
            if (skip) {skip = false}
            else callback();
            time=t;
          }
        });
      }, 3000);
    },
    skipNext() {skip = true;},
    kill() {if (timer) clearInterval(timer);}
  }
}

export function FoldersWatcher(paths: string[], callback: Function) {
  let time = <number[]>[];
  let timer: number; 

  paths.forEach((p) => invoke<number>('timestamp',{ path: p }).then((t)=>time.push(t)));

  timer = setInterval(() => {
    for (let i=0;i<paths.length;i++) {
      invoke<number>('timestamp',{ path: paths[i] }).then((t)=>{
        if (t>time[i]) {
          callback();
          clearInterval(timer);
        }
      });
    }
  }, 3000);
}

export async function env(arg: string) {
  const output = await new Command('bash', ['-ilc','env']).execute();
  let res = '';
  if (output.code==0) {
    let m = output.stdout.match(new RegExp(`${arg}=(.*)\n`));
    if (m) res = m[1];
  }
  return res;
}

export default {
  wrapper,
}