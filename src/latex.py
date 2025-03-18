from PyQt5.QtCore import QRegExp, QProcess, QFileSystemWatcher
from subprocess import PIPE, Popen
import os, re

import settings
from autocompleter import ref, cite

def build_pdf(main, weak=True):
    cmd = settings.app['compiler']['weak'] if weak else settings.app['compiler']['hard']
    root = os.path.dirname(main)
    file = os.path.basename(main).replace('.tex','')
    p = Popen(f'cd {root}; {cmd} {file}', shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    print(stdout, stderr)
    if p.wait() != 0:
        return False
    return True

class Compiler:
    def __init__(self, callback):
        self.p = None
        self.callback = callback

    def __call__(self, main, weak):
        cmd = settings.app['compiler']['weak'] if weak else settings.app['compiler']['hard']
        root = os.path.dirname(main)
        file = os.path.basename(main).replace('.tex','')

        if self.p is None:
            self.p = QProcess()
            self.p.finished.connect(self.callback)

# class FileBase:
#     def __init__(self, filename):
#         self.root = os.path.dirname(filename)
#         self.base = os.path.basename(filename)
#         self.filename = filename
#         self.data = []
#         self.completer = None
#         self.linked = False

#     def setLinked(self, bool):
#         self.linked = bool

#     def __call__(self):
#         text = open(self.filename, 'r').read()

#         toremove = list(self.data)

#         if self.linked:
#             re = QRegExp(self.regexp)
#             re.setMinimal(True)
#             index = re.indexIn(text)
#             while index >= 0:
#                 word = re.cap(1)
#                 if not word in self.data:
#                     self.data.append(word)
#                     # self.completer.update_keyword(word, remove=False)
#                     self.completer.add_keyword(self.filename, word)
#                 else:
#                     toremove.remove(word)
#                 index = re.indexIn(text, index + 9 + len(word))

#         for r in toremove:
#             self.data.remove(r)
#             # self.completer.update_keyword(r, remove=True)
#             self.completer.remove_keyword(self.filename, word)

#         # print(self.__dict__)

#     def __del__(self):
#         self.completer.delete(self.filename)
#         del self.data

# class TexFile2(FileBase):
#     def __init__(self, filename):
#         super().__init__(filename)
#         self.completer = ref
#         self.regexp = "\\label\{([^{]*)\}"
        
    
# class BibFile(FileBase):
#     def __init__(self, filename):
#         super().__init__(filename)
#         self.completer = cite
#         self.regexp = "@article\{(.*),"

class BibFile:
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.filename)
        self.watcher.fileChanged.connect(self.__call__)
        
        # self.completer = cite

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
                    self.data[tag] = _content

        cite.delete(self.filename)
        cite.extend(self.filename, list(self.data.keys()))

class TexFile:
    class TexCmd:
        def __init__(self, tag, square, curly, file, line):
            self.tag = tag
            self.square = square
            self.curly = curly
            self.location = [file, line]
        
    def __init__(self, filename):
        self.filename = os.path.abspath(filename)
        self.root = os.path.dirname(self.filename)
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.filename)
        self.watcher.fileChanged.connect(self.__call__)
        
        # self.completer = ref

        self.children = {}

        self()

    def __call__(self):
        self.data = {}
        toadd = []
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
                        fname = _arg2 if _arg2[0]=='/' else os.path.join(self.root, _arg2)
                        self.data[tag].append(fname)
                        if not fname in self.children:
                            self.children[fname] = TexFile(fname) if tag=='input' else BibFile(fname)
                        else:
                            toremove.remove(fname)
                else:
                    self.data[tag].append(
                        self.TexCmd(tag, None if arg1 is None else arg1[1:-1], arg2, self.filename, i)
                    )
            
        ref.delete(self.filename)
        ref.extend(self.filename, [d.curly for d in self.data['label']])

        for tag in ('input', 'bibliography'):
            if not tag in self.data:
                self.data[tag] = []

        for r in toremove:
            del self.children[r]

    def __del__(self):
        ref.delete(self.filename)