# Starter code for implementing mean-shift clustering.
# Marc Feldman (mfeldm21)
# Jonathan Liu (jliu118)

# https://github.com/paolo-f/bcfind/blob/master/bcfind/mscd.py
# In this, they have a variable bandwidth. Need to figure out what that 
# is for us because it is used to find threshold value.

import numpy as np

# seeds: set of seeds (described in Section 2.2.4)
# points: set of voxels whose intensity exceeds the background threshold
# radius: is the radius used for the kernel
# bandwidth: is a value that allows us to change the convergence threshold
def cluster(seeds, points, radius, bandwidth = 1):
    Z = 0
    for point in points:
        Z += point[3]

    C_set = set()

    for seed in seeds:
        converged = False

        while not converged:
            prev_seed = seed
            new_seed = np.zeros(len(seed))
            for point in points:
                new_seed += (point[3] * point * spherical_kernel(prev_seed - point, radius)) / Z
            converged = check_converged(new_seed, prev_seed, bandwidth)
        C_set.add(new_seed)
    return C_set


    # for p in seeds:
    #     c = p
    #     converged = False
    #     # not sure if implemented correctly?
    #     while not converged:
    #         prev = c
    #         c = np.zeros(len(c))
    #         for q in points:
    #             c += (intensities[q] * q * spherical_kernel(prev - q, radius)) / Z
    #         converged = check_converged(c, prev, bandwidth)
    #     C_set.add(c)
    # return C_set


# used to see if a voxel has converged yet
# voxel_1 is the voxel after the most recent update
# voxel_2 is the voxel prior to the most recent update
# bandwidth allows us to change how we want our data to converge
def check_converged(voxel_1, voxel_2, bandwidth):
    dist = np.linalg.norm(voxel_1 - voxel_2)
    if abs(dist) < .001 * bandwidth:    
        return True
    return False                        


# a is the voxel
# R is a parameter that should be smaller than the expected radius of a cell
def spherical_kernel(a, R):
    if np.linalg.norm(a) < R:
        return 1
    return 0