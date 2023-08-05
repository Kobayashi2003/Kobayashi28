import numpy as np
from utils.features import prepare_for_training

class LinearRegression:
    def __init__(self, data, labels, polynomial_degree=0, sinusoid_degree=0, normalize_data=True):
        """
        1. Prepare data for training
        2. Get number of features
        3. Initialize parameters matrix
        """
        (data_prosecced, features_mean, features_deviation) = prepare_for_training(data, polynomial_degree, sinusoid_degree, normalize_data)

        self.data = data_prosecced
        self.labels = labels
        self.features_mean = features_mean
        self.features_sdeviation = features_deviation
        self.polynomial_degree = polynomial_degree
        self.sinusoid_degree = sinusoid_degree
        self.normalize_data = normalize_data

        num_features = self.data.shape[1]
        self.theta = np.zeros((num_features, 1))

    def train(self, alpha, num_iterations = 500):
        cost_history = self.gradient_descent(alpha, num_iterations)
        return self.theta, cost_history

    def gradient_descent(self, alpha, num_iterations):
        cost_history = []
        for _ in range(num_iterations):
            self.gradient_step(alpha) 
            cost_history.append(self.cost_function(self.data, self.labels))
        return cost_history

    def gradient_step(self, alpha):
        """
        gradient_step: update theta using one step of gradient descent
        """
        num_samples = self.data.shape[0]
        predictions = LinearRegression.hypothesis(self.data, self.theta)
        delta = predictions - self.labels
        self.theta = self.theta - (alpha / num_samples) * np.dot(self.data.T, delta)

    def cost_function(self, data, labels):
        num_examples = data.shape[0]
        delta = LinearRegression.hypothesis(data, self.theta) - labels
        cost = 1 / (2 * num_examples) * np.dot(delta.T, delta)
        return cost[0][0]

    @staticmethod
    def hypothesis(data, theta):
        if data.shape[1] != theta.shape[0]:
            raise ValueError('Number of features in data and theta must be equal')
        predictions = np.dot(data, theta)
        return predictions
    
    def get_cost(self, data, labels):
        data_processed = prepare_for_training(data, self.polynomial_degree, self.sinusoid_degree, self.normalize_data)[0]
        return self.cost_function(data_processed, labels)
    
    def predict(self, data):
        data_processed = prepare_for_training(data, self.polynomial_degree, self.sinusoid_degree, self.normalize_data)[0]
        return LinearRegression.hypothesis(data_processed, self.theta)