from numpy import empty
from itertools import product
import serpentTools
d = serpentTools.readDataFile('bwr_det0.m')['xymesh']

# Get data

xgrids = d.grids['X']
ygrids = d.grids['Y']

nx = xgrids.shape[0]
ny = ygrids.shape[0]

data = empty((nx * ny, 5)) # x, y, z, fast, thermal
data[:, 2].fill(0)

for ix, (yi, xi) in enumerate(product(range(ny), range(nx))):
    data[ix, 0] = xgrids[xi, 1]
    data[ix, 1] = ygrids[yi, 1]
    data[ix, 3] = d.tallies[0, yi, xi]
    data[ix, 4] = d.tallies[1, yi, xi]

with open('bwr.csv', 'w') as out:
    out.write("X Axis,Y Axis,Z Axis,Fast,Thermal\n")
    for row in data:
        out.write(','.join(map(str, row)) + "\n")

