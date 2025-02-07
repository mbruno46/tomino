from subprocess import PIPE, Popen
import os
import settings

def build_pdf(main, weak=True):
    cmd = settings.app['compiler']['weak'] if weak else settings.app['compiler']['hard']
    root = os.path.dirname(main)
    file = os.path.basename(main).replace('.tex','')
    p = Popen(f'cd {root}; {cmd} {file}', shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    print(stdout)
    if stderr!='':
        print(stderr)

