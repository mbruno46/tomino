import { ref, reactive } from 'vue'

export interface LooseObject {
  [key: string]: any
}

function _editor() {
  const files = reactive<LooseObject>({});
  var selected = '';
  
  function focusFile(name: string) {
    if (name in files) {
      if (selected in files) files[selected].open = false;
      files[name].open = true;
      selected = name;
    }
  }

  return {
    files,
    focusFile,
    openFile(path: string, name: string) {
      if (!(name in files)) {
        files[name] = {
          path: path,
          open: true,
          modified: false,
        }
      }
      focusFile(name);
    },
    closeFile(name: string) {
      if (name in files) delete files[name];
      if (selected==name) {
        if (Object.keys(files)[0]) {
          selected = Object.keys(files)[0];
          files[selected].open =true;
        }
      }
    },
  }
}

var Editor = _editor();

const pdf = ref({
  cwd: '',
  main: '',
  compile: 0,
  refresh: false,
  loader: false,
});

export default {
  pdf,
  Editor,
}