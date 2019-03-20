from numpy import empty_like, add, empty
from runner import Runner

r = Runner('template', './sss2')

def searchMaxKinf(x, *args):
    runner = args[0]

    keff, unc = runner.run(x[0], args[1])
    print(x, keff)
    return -keff

def getRangeKeff(runner, fRads, mRads=None):
    if mRads is None:
        mRads = empty_like(fRads)
        mRads.fill(0.63)
    keffVec = empty_like(fRads, dtype=float)
    uncVec = empty_like(keffVec)

    for ix, (fp, mp) in enumerate(zip(fRads, mRads)):
        keffVec[ix], uncVec[ix] = runner.run(fp, mp)
    return keffVec, uncVec

