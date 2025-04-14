import numpy as np

class PCA:
    """
    Principal Component Analysis implementation
    """
    def __init__(self, n_components):
        self.n_components = n_components
        self.mean = None
        self.components = None
        self.explained_variance_ = None
    
    def fit(self, X):
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
        
        cov_matrix = (X_centered.T @ X_centered) / (X_centered.shape[0] - 1)
        
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        eigenvalues = np.real(eigenvalues)
        eigenvectors = np.real(eigenvectors)
        
        idx = np.argsort(eigenvalues)[::-1]
        self.explained_variance_ = eigenvalues[idx]
        # Store eigenvectors as rows for easier access to individual components
        self.components = eigenvectors[:, idx[:self.n_components]].T
        
        return self
    
    def transform(self, X):
        return (X - self.mean) @ self.components.T
    
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    
    def get_component(self, idx):
        """
        Get a specific principal component (useful for visualization)
        
        Parameters:
        -----------
        idx : int
            Index of the component to retrieve
        
        Returns:
        --------
        component : array
            The requested principal component
        """
        if idx >= self.components.shape[0]:
            raise IndexError(f"Component index {idx} out of bounds")
        return self.components[idx] 