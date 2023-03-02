import { listen } from '@tauri-apps/api/event';
import { invoke } from '@tauri-apps/api/tauri';

export function wrapper(name:string, f: Function) {
  (async ()=> {
    const out = await listen(name, ()=>{f()});
  })();
}


export function FileWatcher(callback: Function) {
  let time = 0;
  let skip = false;
  let timer: number; 

  return {
    init(path: string) {
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

export default {
  wrapper,
}