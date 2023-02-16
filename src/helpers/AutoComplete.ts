
const rcmds = RegExp(/^.*(\\\w+)$/)
const rargs = RegExp(/^.*(\\\w+)(?:\[.*\])?{([^}]*)$/)
const cmds = [
  '\\begin',
  '\\bibliography',
  '\\bibliographystyle',
  '\\bibitem',
];
const envs = [
  'equation',
  'enumerate',
]

function _filter(list: String[], word: string) {
  return list.filter(e => e.substring(0,word.length)==word)
}

export function Suggestions(text: string): {word: String, suggestions: String[]} {
  if (text.match(rcmds)) {
    let w = text.match(rcmds)![1];
    return {word: w, suggestions: _filter(cmds, w)}
  }
    
  // let m = text.match(rargs);
  // if (m==undefined) {return []}

  // switch (m[1]) {
  //   case '\\begin':
  //   case '\\end':
  //     return _filter(envs, m[2]);
  // }

  return {word:'', suggestions: []};
}