import math
import sys
import numpy as np

MIN_DISTANCE = 0.000001


# MIN_DISTANCE = 0.4

def ms_cluster(points, kernel_bandwidth=1):
    shift_points = points
    max_min_dist = 1
    prev_max_min_dist = 0
    iteration_number = 0

    # points.shape[0] is the number of points
    # still_shifting is initialized to an array of True values.
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
    # group_assignments = group_points(shift_points.tolist())
    # iteration_number += 1
    # return MeanShiftResult(points, shift_points, group_assignments)


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




def group_points(self, points):
    group_assignment = []
    groups = []
    group_index = 0
    index = 0
    for point in points:
        nearest_group_index = self._determine_nearest_group(point, groups)
        if nearest_group_index == None:
            # create new group
            groups.append([point])
            group_assignment.append(group_index)
            group_index += 1
        else:
            group_assignment.append(nearest_group_index)
            groups[nearest_group_index].append(point)
        index += 1
    return np.array(group_assignment)

def determine_nearest_group(self, point, groups):
    nearest_group_index = None
    index = 0
    for group in groups:
        distance_to_group = self._distance_to_group(point, group)
        if distance_to_group < GROUP_DISTANCE_TOLERANCE:
            nearest_group_index = index
        index += 1
    return nearest_group_index

def distance_to_group(self, point, group):
    min_distance = sys.float_info.max
    for pt in group:
        dist = euc_dist(point, pt)
        if dist < min_distance:
            min_distance = dist
    return min_distance