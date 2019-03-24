from matplotlib.pyplot import pcolormesh
from .coe2frame import buildFrame

def setupCollector(col):
    if not col.xsTables:
        col.collect()
    col.states = (
        (300., 750.),
        (300., 600.),
        (1200., 300., 900.,),
    )
    col.axis = ("Univ", "Coolant Dens", "Coolant Temp", "Fuel Temp", "Burnup", "Group")


def plotDepmtxStructure(mtx):
    orig = mtx.data.copy()

    mtx.data[mtx.data < 0] = -1
    mtx.data[mtx.data > 0] = 1

    out = pcolormesh(mtx.toarray()[::-1], cmap='PuOr_r')

    mtx.data = orig

    return out
