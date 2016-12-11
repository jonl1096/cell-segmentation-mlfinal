# Starter code for implementing mean-shift clustering.
# Marc Feldman (mfeldm21)
# Jonathan Liu (jliu118)

# https://github.com/paolo-f/bcfind/blob/master/bcfind/mscd.py
# In this, they have a variable bandwidth. Need to figure out what that 
# is for us because it is used to find threshold value.

import numpy as np

R = 0 # need some sort of value for R here, determined somewhere else
      # see comment for spherical_kernel

bandwidth = 1 # need some value here...

# S set of seeds (described in Section 2.2.4)
# L set of voxels whose intensity exceeds the background threshold
# m returns the intensity of a voxel
def cluster(S, L, m):
    global R
    Z = 0
    for p in L:
        Z += m.get(p)   # m returns the intensity of a voxel
                        # This is pseudocodey here, can't use p as key

    C_set = set()

    for p in S:
        c = p
        converged = False
        # not sure if implemented correctly?
        while not converged:
            prev = c
            c = np.zeros(len(c))
            for q in L:
                c += (m.get(q) * q * spherical_kernel(prev - q, R)) / Z
            converged = check_converged(c, prev)
        C_set.add(c)
    return C_set


# used to see if a voxel has converged yet
# voxel_1 is the voxel after the most recent update
# voxel_2 is the voxel prior to the most recent update
def check_converged(voxel_1, voxel_2):
    global bandwidth
    diff = voxel_1 - voxel_2
    for item in diff:
        if not abs(item) < .001 * bandwidth:    # need some threshold value (not sure if this is 
            return False                        # right, but we need some way to check convergence)


# a is the voxel
# R is a parameter that should be smaller than the expected radius of a cell
def spherical_kernel(a, R):
    if np.linalg.norm(a) < R:
        return 1
    return 0