import numpy as np

class PCA:
    """
    Principal Component Analysis implementation
    Reduces dimensionality by projecting data onto principal components
    """
    def __init__(self, n_components):
        """
        Initialize PCA with the number of components to keep
        
        Parameters:
        -----------
        n_components : int
            Number of principal components to keep
        """
        self.n_components = n_components
        self.mean = None
        self.components = None
        self.explained_variance_ = None
    
    def fit(self, X):
        """
        Fit the PCA model with the input data
        
        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Training data
            
        Returns:
        --------
        self : object
            Returns self for chaining
        """
        # Center the data
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
        
        # Calculate covariance matrix
        cov_matrix = (X_centered.T @ X_centered) / (X_centered.shape[0] - 1)
        
        # Eigenvalue decomposition - using eig instead of eigh to handle potential non-symmetric cases
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # Ensure eigenvalues and eigenvectors are real
        eigenvalues = np.real(eigenvalues)
        eigenvectors = np.real(eigenvectors)
        
        # Sort eigenvalues in descending order
        idx = np.argsort(eigenvalues)[::-1]
        self.explained_variance_ = eigenvalues[idx]
        self.components = eigenvectors[:, idx[:self.n_components]]
        
        # Return self for chaining
        return self
    
    def transform(self, X):
        """
        Transform X by projecting it onto the principal components
        
        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Data to transform
            
        Returns:
        --------
        X_transformed : array-like, shape (n_samples, n_components)
            Transformed data
        """
        return (X - self.mean) @ self.components
    
    def fit_transform(self, X):
        """
        Fit the model with X and apply dimensionality reduction
        
        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Training data
            
        Returns:
        --------
        X_transformed : array-like, shape (n_samples, n_components)
            Transformed data
        """
        self.fit(X)
        return self.transform(X) 