import os
import subprocess


def _parse_records(stdout):
    records = []
    current = {}
    for line in stdout.splitlines():
        if ':' not in line:
            continue
        key, _, val = line.partition(':')
        if key in current:
            records.append(current)
            current = {}
        current[key] = val
    if current:
        records.append(current)
    return records


class Synctex:
    def forward(self, tex_file, line, column, pdf_file):
        try:
            p = subprocess.run(
                ['synctex', 'view', '-i', f'{line}:{column}:{tex_file}', '-o', pdf_file],
                capture_output=True, text=True)
        except FileNotFoundError:
            return None

        if p.returncode != 0:
            return None

        records = _parse_records(p.stdout)
        if not records:
            return None

        r = records[0]
        if not all(k in r for k in ('Page', 'x', 'y')):
            return None

        return int(r['Page']), float(r['x']), float(r['y'])

    def backward(self, pdf_file, page, x, y):
        try:
            p = subprocess.run(
                ['synctex', 'edit', '-o', f'{page}:{x}:{y}:{pdf_file}'],
                capture_output=True, text=True)
        except FileNotFoundError:
            return None

        if p.returncode != 0:
            return None

        records = _parse_records(p.stdout)
        if not records:
            return None

        r = records[0]
        if not all(k in r for k in ('Input', 'Line')):
            return None

        return os.path.normpath(r['Input']), int(r['Line'])
