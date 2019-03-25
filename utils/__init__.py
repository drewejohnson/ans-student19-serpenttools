from matplotlib.pyplot import pcolormesh

def plotDepmtxStructure(mtx):
    orig = mtx.data.copy()

    mtx.data[mtx.data < 0] = -1
    mtx.data[mtx.data > 0] = 1

    out = pcolormesh(mtx.toarray()[::-1], cmap='PuOr_r')

    mtx.data = orig

    return out
