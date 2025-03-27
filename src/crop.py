import pymupdf
import sys

fn = sys.argv[1]

doc = pymupdf.open(fn)
page = doc[0] # get the 1st page of the document
bbox = page.bound()
page.set_trimbox(page.bound())
print(page.get_svg_image())
# doc.save(fn.replace('.pdf', '_1.pdf'))