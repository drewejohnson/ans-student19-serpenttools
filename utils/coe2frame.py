"""
Convert a coefficient file to a pandas DataFrame
"""

from numpy import empty, empty_like
from pandas import DataFrame

def unravelUnivData(xsMtx, states):

    shape = xsMtx.shape
    nCols = len(shape)
    nRows = xsMtx.size
    valueTable = empty((nRows, nCols), dtype=float)

    for rowx in range(nRows):
        start = rowx
        for colc in reversed(range(nCols)):
            start, mod = divmod(start, shape[colc])
            valueTable[rowx, colc] = states[colc][mod]

    return xsMtx.ravel(), valueTable


def buildFrame(univ, xsKey):
    xsT = univ.xsTables[xsKey]
    ravelStates = tuple(univ.states) + (
            tuple(univ.burnups), tuple(range(xsT.shape[-1])))
    longXs, longPerts = unravelUnivData(xsT, ravelStates)
    frame = DataFrame(longPerts, columns=univ.axis)
    xsLabel = empty_like(longXs, dtype='<U{}'.format(len(xsKey)))
    xsLabel.fill(xsKey)
    frame.insert(len(univ.axis), "Name", xsLabel)
    frame.insert(len(univ.axis), "XS", longXs)
    return frame
