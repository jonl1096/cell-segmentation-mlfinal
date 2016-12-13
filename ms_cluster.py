import math
import sys
import numpy as np

MIN_DISTANCE = 0.000001


def ms_cluster(points, kernel_bandwidth=1):
    shift_points = points
    max_min_dist = 1
    prev_max_min_dist = 0

    still_shifting = [True] * points.shape[0]
    while max_min_dist > MIN_DISTANCE:
        print max_min_dist

        if max_min_dist == prev_max_min_dist:
            break

        prev_max_min_dist = max_min_dist
        max_min_dist = 0
        for i in range(0, len(shift_points)):
            if not still_shifting[i]:
                continue
            p_new = shift_points[i]
            p_new_start = p_new
            p_new = shift_point(p_new, points, kernel_bandwidth)
            dist = euc_dist(p_new, p_new_start)
            if dist > max_min_dist:
                max_min_dist = dist
            if dist < MIN_DISTANCE:
                still_shifting[i] = False
            shift_points[i] = p_new

    return shift_points

def shift_point(point, points, kernel_bandwidth):
    # from http://en.wikipedia.org/wiki/Mean-shift
    points = np.array(points)
    # numerator
    point_distances = np.sqrt(((point - points) ** 2).sum(axis=1))
    point_weights = gaussian_kernel(point_distances, kernel_bandwidth)
    tiled_weights = np.tile(point_weights, [len(point), 1])
    # denominator
    denominator = sum(point_weights)
    shifted_point = np.multiply(tiled_weights.transpose(), points).sum(axis=0) / denominator
    return shifted_point


def gaussian_kernel(distance, bandwidth):
    val = (1 / (bandwidth * math.sqrt(2 * math.pi))) * np.exp(-0.5 * ((distance / bandwidth)) ** 2)
    return val


def euc_dist(vect1, vect2):
    """ Find and returns the euclidian distance between 2 numpy arrays. """
    return np.linalg.norm(vect1 - vect2)


