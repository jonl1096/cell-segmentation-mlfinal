# Starter code for implementing mean-shift clustering.
# Marc Feldman (mfeldm21)
# Jonathan Liu (jliu118)

import numpy as np

R = 0 # need some sort of value for R here, determined somewhere else
      # see comment for spherical_kernel

# S set of seeds (described in Section 2.2.4)
# L set of voxels whose intensity exceeds the background threshold
# m returns the intensity of a voxel
def cluster(S, L, m):
    global R
    Z = 0
    for p in L:
        Z += m.get(p)   # m returns the intensity of a Voxel
                        # This is pseudocodey here, can't use p as key

    C_set = set()

    for p in S:
        c = p
        converged = False
        while not converged:
            prev = c
            c = np.zeros(len(c))
            for q in L:
                c += (m.get(q) * q * spherical_kernel(prev - q, R)) / Z
            converged = check_converged(c, prev)
        C_set.add(c)
    return C_set


def check_converged(c, prev):
    test = c - prev
    for item in test:
        if not abs(item) < .001:    # need some threshold value (not sure if this is 
            return False            # right, but we need some way to check convergence)


# a is the vector
# R is a parameter that should be smaller than the expected radius of a cell
def spherical_kernel(a, R):
    if np.linalg.norm(a) < R:
        return 1
    return 0