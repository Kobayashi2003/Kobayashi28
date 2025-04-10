import numpy as np
from collections import Counter

class KNN:
    """
    K-Nearest Neighbors classifier implementation
    Classifies based on k closest training samples
    """
    def __init__(self, k=5):
        """
        Initialize KNN with the number of neighbors to use
        
        Parameters:
        -----------
        k : int, default=5
            Number of neighbors to use for classification
        """
        self.k = k
    
    def fit(self, X_train, y_train):
        """
        Fit the KNN model with the training data
        
        Parameters:
        -----------
        X_train : array-like, shape (n_samples, n_features)
            Training data
        y_train : array-like, shape (n_samples,)
            Target values
            
        Returns:
        --------
        self : object
            Returns self for chaining
        """
        self.X_train = X_train
        self.y_train = y_train
        return self
    
    def predict(self, X_test):
        """
        Predict the class labels for the input samples
        
        Parameters:
        -----------
        X_test : array-like, shape (n_samples, n_features)
            Test samples
            
        Returns:
        --------
        y_pred : array-like, shape (n_samples,)
            Predicted class labels
        """
        y_pred = []
        for x in X_test:
            # Calculate Euclidean distance between current sample and all training samples
            distances = np.linalg.norm(self.X_train - x, axis=1)
            # Get indices of k nearest neighbors
            k_indices = np.argsort(distances)[:self.k]
            # Get labels of k nearest neighbors
            k_labels = self.y_train[k_indices]
            # Find the most common label
            most_common = Counter(k_labels).most_common(1)
            y_pred.append(most_common[0][0])
        return np.array(y_pred)
    
    def score(self, X_test, y_test):
        """
        Return the accuracy on the given test data and labels
        
        Parameters:
        -----------
        X_test : array-like, shape (n_samples, n_features)
            Test samples
        y_test : array-like, shape (n_samples,)
            True labels for X_test
            
        Returns:
        --------
        score : float
            Accuracy of the classifier
        """
        y_pred = self.predict(X_test)
        return np.sum(y_pred == y_test) / len(y_test) 