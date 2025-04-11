import numpy as np
from sklearn.svm import SVC

class SVMClassifier:
    def __init__(self, kernel='rbf', C=1.0, gamma='scale'):
        """
        Initialize SVM classifier
        
        Args:
            kernel: Kernel type to be used in the algorithm
            C: Regularization parameter
            gamma: Kernel coefficient
        """
        self.kernel = kernel
        self.C = C
        self.gamma = gamma
        self.svm = SVC(kernel=kernel, C=C, gamma=gamma, probability=True)
        self.is_fitted = False
        
    def fit(self, X, y):
        """
        Fit SVM model to data
        
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
        
        self.svm.fit(X_reshaped, y)
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
            raise ValueError("SVM model must be fitted before predicting")
        
        # Reshape image data to 2D if needed
        if len(X.shape) > 2:
            n_samples = X.shape[0]
            X_reshaped = X.reshape(n_samples, -1)
        else:
            X_reshaped = X
            
        return self.svm.predict(X_reshaped)
        
    def predict_proba(self, X):
        """
        Predict class probabilities for samples in X
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            y_proba: Predicted class probabilities
        """
        if not self.is_fitted:
            raise ValueError("SVM model must be fitted before predicting probabilities")
        
        # Reshape image data to 2D if needed
        if len(X.shape) > 2:
            n_samples = X.shape[0]
            X_reshaped = X.reshape(n_samples, -1)
        else:
            X_reshaped = X
            
        return self.svm.predict_proba(X_reshaped)
