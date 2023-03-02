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
            if (!skip) callback();
            time=t;
          }
        });
      }, 1000);
    },
    skipNext() {skip = true;},
    kill() {clearInterval(timer);}
  }
}

export default {
  wrapper,
}