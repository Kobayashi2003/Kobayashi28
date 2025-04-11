import numpy as np
from sklearn.decomposition import PCA

class PCAdimReducer:
    def __init__(self, n_components=0.95):
        """
        Initialize PCA dimension reducer
        
        Args:
            n_components: Number of components or variance ratio to keep
        """
        self.n_components = n_components
        self.pca = PCA(n_components=n_components)
        self.is_fitted = False
        
    def fit(self, X):
        """
        Fit PCA model to data
        
        Args:
            X: Input data of shape (n_samples, n_features)
        """
        # Reshape image data to 2D if needed
        if len(X.shape) > 2:
            n_samples = X.shape[0]
            X_reshaped = X.reshape(n_samples, -1)
        else:
            X_reshaped = X
        
        self.pca.fit(X_reshaped)
        self.is_fitted = True
        return self
        
    def transform(self, X):
        """
        Apply dimension reduction to X
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            X_transformed: Transformed data
        """
        if not self.is_fitted:
            raise ValueError("PCA model must be fitted before transforming data")
        
        # Reshape image data to 2D if needed
        if len(X.shape) > 2:
            n_samples = X.shape[0]
            X_reshaped = X.reshape(n_samples, -1)
        else:
            X_reshaped = X
            
        return self.pca.transform(X_reshaped)
        
    def fit_transform(self, X):
        """
        Fit PCA model and apply dimension reduction in one step
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            X_transformed: Transformed data
        """
        return self.fit(X).transform(X)
        
    def get_components(self):
        """
        Get the principal components
        
        Returns:
            components: Principal components
        """
        if not self.is_fitted:
            raise ValueError("PCA model must be fitted before getting components")
        
        return self.pca.components_
        
    def get_explained_variance_ratio(self):
        """
        Get the explained variance ratio for each component
        
        Returns:
            explained_variance_ratio: Explained variance ratio
        """
        if not self.is_fitted:
            raise ValueError("PCA model must be fitted before getting explained variance")
        
        return self.pca.explained_variance_ratio_
