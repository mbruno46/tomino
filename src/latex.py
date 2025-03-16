from PyQt5.QtCore import QRegExp, QProcess
from subprocess import PIPE, Popen
import os
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

class FileBase:
    def __init__(self, filename):
        self.root = os.path.dirname(filename)
        self.base = os.path.basename(filename)
        self.filename = filename
        self.data = []
        self.completer = None
        self.linked = False

    def setLinked(self, bool):
        self.linked = bool

    def __call__(self):
        text = open(self.filename, 'r').read()

        toremove = list(self.data)

        if self.linked:
            re = QRegExp(self.regexp)
            re.setMinimal(True)
            index = re.indexIn(text)
            while index >= 0:
                word = re.cap(1)
                if not word in self.data:
                    self.data.append(word)
                    self.completer.update_keyword(word, remove=False)
                else:
                    toremove.remove(word)
                index = re.indexIn(text, index + 9 + len(word))

        for r in toremove:
            self.data.remove(r)
            self.completer.update_keyword(r, remove=True)

        # print(self.__dict__)

    def __del__(self):
        for el in self.data:
            self.completer.update_keyword(el, remove=True)
        del self.data

class TexFile(FileBase):
    def __init__(self, filename):
        super().__init__(filename)
        self.completer = ref
        self.regexp = "\\label\{([^{]*)\}"
        
    
class BibFile(FileBase):
    def __init__(self, filename):
        super().__init__(filename)
        self.completer = cite
        self.regexp = "@article\{(.*),"

