export function debounce<T extends Function>(callback: T, timeout = 300){
  let timer = 0;
  return <T>(...args: any) => {
    clearTimeout(timer);
    timer = setTimeout(() => {callback(...args)}, timeout);
  };
}

export default {
  debounce,
}