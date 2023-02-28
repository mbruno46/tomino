import { listen } from '@tauri-apps/api/event';

export function wrapper(name:string, f: Function) {
  (async ()=> {
    const out = await listen(name, ()=>{f()});
  })();
}

export default {
  wrapper,
}