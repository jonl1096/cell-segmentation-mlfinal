import math
from copy import deepcopy
from cs475_types import Predictor

class LambdaMeans(Predictor):
    def __init__(self, cluster_lambda, clustering_training_iterations, instances, max_index):
        self.cluster_iterations = clustering_training_iterations
        self.max_index = max_index          # max index of a feature in our data
        average_instance = [0] * max_index  # create the first cluster
        for i in range(max_index):
            average_instance[i] = instances[0]._feature_vector.get(i)
        for i in range(1, len(instances)):
            curr_instance = instances[i]
            for feature in curr_instance._feature_vector.keys():
                average_instance[feature] += curr_instance._feature_vector.get(feature)
        for i in range(max_index): 
            average_instance[i] /= len(instances)
        self.cluster_means = []             # stores clusters
        self.cluster_means.append(average_instance)
        self.num_clusters = 1               # number of clusters
        if cluster_lambda > 0:
            self.cluster_lambda = cluster_lambda
        else:
            cluster_lambda = 0
            for instance in instances:
                cluster_lambda += self.distance(average_instance, instance._feature_vector) ** 2
            self.cluster_lambda = cluster_lambda / len(instances)
        self.instance_best_dist = -1        # stores the distance to cluster for last instance looked at


    def train(self, instances):
        for i in range(self.cluster_iterations):
            r_nk = [] # stores cluster each instance is in
            cluster_count = [0] * self.num_clusters
            # E Step
            for a in range(len(instances)):
                instance = instances[a]
                k = self.predict(instance)
                square_dist = self.instance_best_dist ** 2
                if square_dist <= self.cluster_lambda:
                    r_nk.append(k)
                    cluster_count[k] += 1
                else:
                    new_cluster = []
                    for i in range(self.max_index):
                        new_cluster.append(instance._feature_vector.get(i))
                    self.cluster_means.append(new_cluster)
                    r_nk.append(self.num_clusters)
                    self.num_clusters += 1
                    cluster_count.append(1)
            # M Step
            for m in range(self.num_clusters):
                self.cluster_means[m] = [0] * self.max_index
            for x in range(len(instances)):
                cluster = r_nk[x]
                cluster_mean = self.cluster_means[cluster]
                instance = instances[x]
                for feature in instance._feature_vector.keys():
                    cluster_mean[feature] += instance._feature_vector.get(feature) / float(cluster_count[cluster])


    def predict(self, instance):
        best_dist = -1
        for x in range (self.num_clusters):
            cluster_mean = self.cluster_means[x]
            dist = self.distance(cluster_mean, instance._feature_vector)
            if dist < best_dist or best_dist == -1:
                best_dist = dist
                best_cluster = x
        self.instance_best_dist = best_dist  # store best dist for this instance
        return best_cluster


    def distance(self, list_a, vector_b):
        total_sum = 0
        for i in range(self.max_index):
            total_sum += (list_a[i] - vector_b.get(i)) ** 2
        return math.sqrt(total_sum)
