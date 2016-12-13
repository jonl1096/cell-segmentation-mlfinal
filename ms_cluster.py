# Marc Feldman (mfeldm21)
# Jonathan Liu (jliu118)

import math
import numpy as np

def ms_cluster(data, max_index, threshold = .01, bandwidth = 1):
    moved_data = data
    max_min = 1
    prev_max_min = 0

    stopped = [False] * data.shape[0]
    while max_min > threshold && max_min != prev_max_min:
        prev_max_min = max_min
        max_min = 0
        for i in range(0, len(moved_data)):
            if not stopped[i]:
                new_instance_start = moved_data[i]
                new_instance = move_instance(moved_data[i], max_index, data, bandwidth)
                dist = euclidean_distance(new_instance, new_instance_start)
                if dist > max_min:
                    max_min = dist
                if dist < threshold:
                    stopped[i] = True
                moved_data[i] = new_instance
            else:
                continue

    return moved_data

def move_instance(instance, max_index, data, bandwidth):
    data = np.array(data)
    instance_distances = np.sqrt(((instance - data) ** 2).sum(axis = 1))
    weights = gaussian_kernel(instance_distances, bandwidth)
    tiled = np.tile(weights, [max_index, 1])
    shifted_instance = np.multiply(tiled.transpose(), data).sum(axis = 0) / sum(weights)
    return shifted_instance


def gaussian_kernel(distance, bandwidth):
    return (1 / (bandwidth * math.sqrt(2 * math.pi))) * np.exp(-0.5 * ((distance / bandwidth)) ** 2)


def euclidean_distance(array_1, array_2):
    return np.linalg.norm(array_1 - array_2)
