from PyQt6.QtCore import Qt, QThread, pyqtSignal, QFileSystemWatcher, QAbstractItemModel, QModelIndex

from subprocess import PIPE, Popen
import os, re

import settings
from autocompleter import ref, cite

def safe_path(tag, path, root):
    if tag=='input':
        path += '' if path[-4:]=='.tex' else '.tex'
    elif tag=='bibliography':
        path += '' if path[-4:]=='.bib' else '.bib'

    if os.path.exists(path):
        return path
    else:
        fn = os.path.join(root, path)
        if os.path.exists(fn):
            return fn
    return None


class Compiler(QThread):
    success = pyqtSignal(bool)

    def __init__(self, main, weak):
        self.main = main
        self.weak = weak
        super().__init__()

    def run(self):
        cmd = settings.app['compiler']['weak'] if self.weak else settings.app['compiler']['hard']
        root = os.path.dirname(self.main)
        file = os.path.basename(self.main).replace('.tex','')
        p = Popen(f'cd {root}; {cmd} {file}', shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        print(stdout, stderr)
        self.success.emit(False if p.wait() != 0 else True)



class BibFile:
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.filename)
        self.watcher.fileChanged.connect(self.__call__)
        
        self()

    def __call__(self):
        self.data = {}

        text = open(self.filename, 'r').read()
        fmt = r'@(\w+)\{([^@]*)\}'
        patt = re.compile(fmt, re.I|re.U)
        for m in patt.finditer(text.strip()):
            _, content = m.groups()
            tag = content.split(',')[0].strip()
            self.data[tag] = ""

            _fmt = r'(\w+)\s?=\s?(?!\w+\s?=)(.*)'
            _patt = re.compile(_fmt, re.I|re.U)
            for _m in _patt.finditer(content.strip()):
                _tag, _content = _m.groups()
                if _tag == 'title':
                    self.data[tag] = _content.strip(',"{}')

        cite.delete(self.filename)
        cite.extend(self.filename, [f'{key} [{self.data[key]}]' for key in self.data])

    def __del__(self):
        if cite:
            cite.delete(self.filename)

class TexNode:
    def __init__(self, tag, square='', curly='', file='', line=-1):
        self.tag = tag
        self.square = square
        self.curly = curly
        self.location = [file, line]
        self.children = []
        self.parent = None

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def getLastChild(self):
        return self.children[-1]
    
    def hasChildren(self):
        return len(self.children)>0
    
class TexFile:
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        self.root = os.path.dirname(self.filename)
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.filename)
        self.watcher.fileChanged.connect(self.__call__)
        
        self.children = {}

        self()

    def __call__(self):
        self.data = {}
        toremove = list(self.children.keys())

        for i, l in enumerate(open(self.filename,'r').readlines()):
            if re.match('\s?%', l):
                continue
            fmt = r'\\(\w+)(\[[^\]]*\])?\{([^\}]*)\}'
            patt = re.compile(fmt, re.I|re.U)
            for m in patt.finditer(l.strip()):
                tag, arg1, arg2 = m.groups()
                if not tag in self.data:
                    self.data[tag] = []

                if tag in ('input', 'bibliography'):
                    for _arg2 in arg2.split(','):
                        fname = safe_path(tag, _arg2.strip(), self.root)
                        self.data[tag].append(fname)
                        if not fname in self.children:
                            self.children[fname] = TexFile(fname) if tag=='input' else BibFile(fname)
                        else:
                            toremove.remove(fname)
                else:
                    self.data[tag].append(
                        TexNode(tag, None if arg1 is None else arg1[1:-1], arg2, self.filename, i)
                    )
                    if tag in latex_sections:
                        model.populate(tag, self.data[tag][-1])

        for tag in ('input', 'bibliography', 'label'):
            if not tag in self.data:
                self.data[tag] = []
            
        ref.delete(self.filename)
        ref.extend(self.filename, [d.curly for d in self.data['label']])

        for r in toremove:
            del self.children[r]

    def __del__(self):
        if ref:
            ref.delete(self.filename)


class TexModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self, init_string=None):
        if hasattr(self, 'root'):
            del self.root
        self.root = TexNode('part')
        self.root.addChild(TexNode('chapter', curly='Select a main .tex file' if init_string is None else init_string))

    def index(self, row, column, _parent: QModelIndex):
        if column==0:
            parent = _parent.internalPointer() if _parent.isValid() else self.root
            if row<len(parent.children):
                return self.createIndex(row, column, parent.children[row])
        return QModelIndex()
    
    def parent(self, index):
        if index.isValid():
            child = index.internalPointer()
            if not child.parent is None:
                return self.createIndex(child.parent.children.index(child), 0, child.parent)
        return QModelIndex()
    
    def rowCount(self, index: QModelIndex):
        if index.isValid():
            return len(index.internalPointer().children)
        return len(self.root.children)
    
    def columnCount(self, index: QModelIndex):
        return 1
    
    def data(self, index: QModelIndex, role):
        if (role==Qt.ItemDataRole.DisplayRole):
            return index.internalPointer().curly
        return None
    
    def populate(self, tag, child):
        def get_last_child(node: TexNode, level, depth):
            if depth==level:
                return node
            else:
                if not node.hasChildren():
                    node.addChild(TexNode(latex_sections[level]))
                return get_last_child(node.getLastChild(), level+1, depth)
    
        get_last_child(self.root, 0, latex_sections[tag]).addChild(child)


model = TexModel()
latex_sections = {
    'chapter': 0,
    'section': 1,
    'subsection': 2
}
main = None

def init(filename):
    global model
    model.init(os.path.basename(filename))
    global main
    main = TexFile(filename)