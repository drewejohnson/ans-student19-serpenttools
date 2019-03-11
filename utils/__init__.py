from matplotlib.pyplot import pcolormesh
from .coe2frame import buildFrame

def setupCollector(col):
    if not col.xsTables:
        col.collect()
    col.states = (
        (1050., 1200., 600., 750., 900.),
        (650., 675., 700., 725., 750.),
        (500., 700., 800., 600.),
    )
    col.axis = ("Univ", "Fuel T", "Coolant Dens", "Coolant Temp", "Burnup", "Group")


def plotDepmtxStructure(mtx):
    orig = mtx.data.copy()

    mtx.data[mtx.data < 0] = -1
    mtx.data[mtx.data > 0] = 1

    out = pcolormesh(mtx.toarray()[::-1], cmap='PuOr_r')

    mtx.data = orig

    return out
