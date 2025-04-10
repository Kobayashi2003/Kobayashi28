import numpy as np

class LDA:
    """
    Linear Discriminant Analysis implementation
    Reduces dimensionality while preserving class discriminatory information
    """
    def __init__(self, n_components):
        """
        Initialize LDA with the number of components to keep
        
        Parameters:
        -----------
        n_components : int
            Number of components to keep
            Maximum value is (n_classes - 1)
        """
        self.n_components = n_components
        self.W = None
        self.mean = None
    
    def fit(self, X, y):
        """
        Fit the LDA model with the input data
        
        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Training data
        y : array-like, shape (n_samples,)
            Target values
            
        Returns:
        --------
        self : object
            Returns self for chaining
        """
        classes = np.unique(y)
        n_features = X.shape[1]
        
        # Calculate global mean
        self.mean = np.mean(X, axis=0)
        
        # Initialize within-class scatter matrix
        Sw = np.zeros((n_features, n_features))
        # Initialize between-class scatter matrix
        Sb = np.zeros((n_features, n_features))
        
        # Calculate class means, within-class scatter and between-class scatter
        for c in classes:
            # Get samples of current class
            Xc = X[y == c]
            # Calculate class mean
            class_mean = np.mean(Xc, axis=0)
            
            # Calculate within-class scatter matrix
            # Centered data for current class
            class_centered = Xc - class_mean
            Sw += class_centered.T @ class_centered
            
            # Calculate between-class scatter matrix
            # Difference between class mean and global mean
            n_c = Xc.shape[0]
            mean_diff = (class_mean - self.mean).reshape(-1, 1)
            Sb += n_c * mean_diff @ mean_diff.T
        
        # Add regularization to avoid singularity issues
        Sw_reg = Sw + np.eye(n_features) * 1e-4
        
        # Solve generalized eigenvalue problem
        try:
            # Calculate eigenvectors and eigenvalues
            eig_vals, eig_vecs = np.linalg.eig(np.linalg.inv(Sw_reg) @ Sb)
            # Use absolute values for complex eigenvalues for sorting
            idx = np.argsort(np.abs(eig_vals))[::-1]
            eig_vals = eig_vals[idx]
            # Keep only real part of eigenvectors for the selected components
            self.W = np.real(eig_vecs[:, idx[:self.n_components]])
        except np.linalg.LinAlgError:
            # If inversion still fails with regularization, increase regularization
            print("Warning: LDA encountered a singular matrix issue, increasing regularization")
            Sw_reg = Sw + np.eye(n_features) * 1e-2
            eig_vals, eig_vecs = np.linalg.eig(np.linalg.inv(Sw_reg) @ Sb)
            idx = np.argsort(np.abs(eig_vals))[::-1]
            self.W = np.real(eig_vecs[:, idx[:self.n_components]])
        
        return self
    
    def transform(self, X):
        """
        Transform X by projecting it onto the linear discriminant components
        
        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Data to transform
            
        Returns:
        --------
        X_transformed : array-like, shape (n_samples, n_components)
            Transformed data
        """
        return X @ self.W 