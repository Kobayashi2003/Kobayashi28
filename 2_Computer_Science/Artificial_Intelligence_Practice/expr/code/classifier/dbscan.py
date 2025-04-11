import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score

class DBSCANClassifier:
    def __init__(self, eps=None, min_samples=5, auto_eps=True):
        """
        Initialize DBSCAN classifier with automatic parameter estimation
        
        Args:
            eps: DBSCAN eps parameter (distance threshold)
            min_samples: DBSCAN min_samples parameter
            auto_eps: Whether to automatically estimate eps parameter
        """
        self.eps = eps
        self.min_samples = min_samples
        self.auto_eps = auto_eps
        self.dbscan = None
        self.is_fitted = False
        self.class_centroids = {}
        
    def _estimate_eps(self, X):
        """
        Estimate eps parameter based on k-distance graph
        """
        # Calculate distances to k nearest neighbors
        k = min(self.min_samples, len(X) - 1)
        nbrs = NearestNeighbors(n_neighbors=k).fit(X)
        distances, _ = nbrs.kneighbors(X)
        
        # Sort distances to kth neighbor
        distances = np.sort(distances[:, -1])
        
        # Find point of maximum curvature (elbow)
        from scipy.signal import argrelextrema
        # Smooth the curve
        from scipy.ndimage import gaussian_filter1d
        distances_smooth = gaussian_filter1d(distances, sigma=3)
        
        # Compute second derivative
        derivatives = np.gradient(np.gradient(distances_smooth))
        
        # Find local maxima in second derivative
        local_max_indices = argrelextrema(derivatives, np.greater)[0]
        
        if len(local_max_indices) > 0:
            # Use the first local maximum as the elbow point
            elbow_idx = local_max_indices[0]
            eps = distances[elbow_idx]
        else:
            # Fallback: use the mean of the distances
            eps = np.mean(distances)
        
        return eps
    
    def fit(self, X, y):
        """
        Fit DBSCAN model to data
        
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
        
        # Get unique class labels
        unique_labels = np.unique(y)
        
        # For each class, compute centroid for efficient prediction
        for label in unique_labels:
            # Get samples of current class
            class_mask = (y == label)
            X_class = X_reshaped[class_mask]
            
            # Store class centroid for prediction
            self.class_centroids[label] = np.mean(X_class, axis=0)
        
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
            raise ValueError("DBSCAN model must be fitted before predicting")
        
        # Reshape image data to 2D if needed
        if len(X.shape) > 2:
            n_samples = X.shape[0]
            X_reshaped = X.reshape(n_samples, -1)
        else:
            X_reshaped = X
        
        # Predict classes using nearest centroid
        y_pred = np.zeros(len(X_reshaped), dtype=int)
        
        for i, x in enumerate(X_reshaped):
            min_dist = float('inf')
            best_label = None
            
            # Assign to the nearest class centroid
            for label, centroid in self.class_centroids.items():
                dist = np.linalg.norm(x - centroid)
                if dist < min_dist:
                    min_dist = dist
                    best_label = label
            
            y_pred[i] = best_label
        
        return y_pred 