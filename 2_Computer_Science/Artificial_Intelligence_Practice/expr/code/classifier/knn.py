import numpy as np
from sklearn.neighbors import KNeighborsClassifier

class KNNClassifier:
    def __init__(self, n_neighbors=5):
        """
        Initialize KNN classifier
        
        Args:
            n_neighbors: Number of neighbors to use for classification
        """
        self.n_neighbors = n_neighbors
        self.knn = KNeighborsClassifier(n_neighbors=n_neighbors)
        self.is_fitted = False
        
    def fit(self, X, y):
        """
        Fit KNN model to data
        
        Args:
            X: Input data of shape (n_samples, n_features)
            y: Target labels of shape (n_samples,)
        """
        # Reshape image data to 2D if needed
        if len(X.shape) > 2:
            n_samples = X.shape[0]
            X_reshaped = X.reshape(n_samples, -1)
        else:
            X_reshaped = X
        
        self.knn.fit(X_reshaped, y)
        self.is_fitted = True
        return self
        
    def predict(self, X):
        """
        Predict class labels for samples in X
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            y_pred: Predicted class labels
        """
        if not self.is_fitted:
            raise ValueError("KNN model must be fitted before predicting")
        
        # Reshape image data to 2D if needed
        if len(X.shape) > 2:
            n_samples = X.shape[0]
            X_reshaped = X.reshape(n_samples, -1)
        else:
            X_reshaped = X
            
        return self.knn.predict(X_reshaped)
        
    def predict_proba(self, X):
        """
        Predict class probabilities for samples in X
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            y_proba: Predicted class probabilities
        """
        if not self.is_fitted:
            raise ValueError("KNN model must be fitted before predicting probabilities")
        
        # Reshape image data to 2D if needed
        if len(X.shape) > 2:
            n_samples = X.shape[0]
            X_reshaped = X.reshape(n_samples, -1)
        else:
            X_reshaped = X
            
        return self.knn.predict_proba(X_reshaped)
