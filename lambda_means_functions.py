max_index = 0

from cs475_types import ClassificationLabel, FeatureVector, Instance, Predictor
from lambda_means import LambdaMeans

def load_data(data):
    global max_index
    instances = []
    for point in data:

        label = ClassificationLabel(0)
        feature_vector = FeatureVector()
            
        for i in range(3):
            if point[i] != 0.0:
                feature_vector.add(i, point[i])

        instance = Instance(feature_vector, label)
        instances.append(instance)

    return instances

def do_lambda_means_clustering(cluster_lambda, clustering_training_iterations, instances):
    global max_index
    predictor = LambdaMeans(cluster_lambda, clustering_training_iterations, instances, max_index)
    predictor.train(instances)