"""Neural Network model."""
import pickle, os, numpy as np
from sklearn.neural_network import MLPClassifier

class NeuralNetworkMusic:
    def __init__(self):
        self.model = MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=200, random_state=42, early_stopping=True)
    def train(self, X, y):
        self.model.fit(X.reshape(X.shape[0], -1), y)
    def predict(self, X):
        return self.model.predict(X.reshape(X.shape[0], -1))
    def score(self, X, y):
        return self.model.score(X.reshape(X.shape[0], -1), y)
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        pickle.dump(self.model, open(path, "wb"))
    def load(self, path):
        self.model = pickle.load(open(path, "rb"))
