from numpy import empty
from itertools import product
import serpentTools
d = serpentTools.read('det_det0.m')['xymesh']

# Get data

xgrids = d.grids['X']
ygrids = d.grids['Y']

nx = xgrids.shape[0]
ny = ygrids.shape[0]

data = empty((nx * ny, 4))
data[:, 2].fill(0)

for ix, (yi, xi) in enumerate(product(range(ny), range(nx))):
    data[ix, 0] = xgrids[xi, 2]
    data[ix, 1] = ygrids[yi, 2]
    data[ix, 3] = d.tallies[yi, xi]

with open('det.csv', 'w') as out:
    out.write("X Axis,Y Axis,Z Axis,Flux\n")
    for row in data:
        out.write(','.join(map(str, row)) + "\n")
