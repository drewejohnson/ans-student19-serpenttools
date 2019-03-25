from matplotlib.pyplot import pcolormesh
from jinja2 import Template

def plotDepmtxStructure(mtx):
    orig = mtx.data.copy()

    mtx.data[mtx.data < 0] = -1
    mtx.data[mtx.data > 0] = 1

    out = pcolormesh(mtx.toarray()[::-1], cmap='PuOr_r')

    mtx.data = orig

    return out

def render(nRings):
    with open("./template.jinja") as stream:
        template = Template(stream.read())
    return template.render(nRings=nRings)
