import pymupdf
import os

fn = '/Users/mbruno/Physics/letters/MorandiG/sign_bruno.pdf'
# fn = '/Users/mbruno/Physics/tomino/dummy/main.tex'

if os.path.exists(fn):
    print('here ')
    doc = pymupdf.open(fn)
    for i, p in enumerate(doc):
        with open(f'page{i}.svg', 'w') as f:
            f.write(p.get_svg_image())
    doc.close()
else:
    print('ouch')
