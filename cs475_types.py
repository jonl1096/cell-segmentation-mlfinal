from abc import ABCMeta, abstractmethod

# abstract base class for defining labels
class Label:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __str__(self): pass

       
class ClassificationLabel(Label):
    def __init__(self, label):
        self.label = label
        
    def __str__(self):
        return str(self.label)

    # get label in int form
    def get(self):
        return self.label


class FeatureVector:
    def __init__(self):
        self.dict = {}
        
    def add(self, index, value):
        self.dict[index] = value
        
    def get(self, index):
        if index in self.dict:
            return self.dict[index]
        return 0

    def keys(self):
        return self.dict.keys()
        

class Instance:
    def __init__(self, feature_vector, label):
        self._feature_vector = feature_vector
        self._label = label

# abstract base class for defining predictors
class Predictor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def train(self, instances): pass

    @abstractmethod
    def predict(self, instance): pass

       
