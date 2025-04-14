import numpy as np

class LDA:
    """
    Linear Discriminant Analysis implementation
    """
    def __init__(self, n_components, tol=1e-4):
        self.n_components = n_components
        self.tol = tol
        self.W = None
        self.mean = None
    
    def fit(self, X, y):
        classes = np.unique(y)
        n_classes = len(classes)
        n_samples, n_features = X.shape
        
        # Calculate class means and frequencies
        class_means = np.zeros((n_classes, n_features))
        class_freqs = np.zeros(n_classes)
        for i, c in enumerate(classes):
            class_mask = (y == c)
            class_freqs[i] = np.sum(class_mask) / n_samples
            class_means[i] = np.mean(X[class_mask], axis=0)
        
        # Calculate global mean
        self.mean = class_freqs @ class_means
        
        # Calculate within-class scatter matrix (Sw)
        within_class_scatter = np.zeros((n_features, n_features))
        for i, c in enumerate(classes):
            # Get samples of current class and center them
            class_samples = X[y == c]
            centered_samples = class_samples - class_means[i]
            
            # Add contribution to within-class scatter
            within_class_scatter += centered_samples.T @ centered_samples
        
        # Calculate between-class scatter matrix (Sb)
        between_class_scatter = np.zeros((n_features, n_features))
        for i, c in enumerate(classes):
            # Get class frequency and mean difference
            n_class_samples = np.sum(y == c)
            mean_diff = (class_means[i] - self.mean).reshape(-1, 1)
            
            # Add weighted contribution to between-class scatter
            between_class_scatter += n_class_samples * mean_diff @ mean_diff.T
        
        # Apply small regularization to avoid singularity if needed
        alpha = 0.001
        within_class_scatter_reg = within_class_scatter + alpha * np.eye(n_features)
        
        # Solve generalized eigenvalue problem: Sb·w = λ·Sw·w
        # Using eigh for symmetric matrices
        eigenvalues, eigenvectors = np.linalg.eigh(
            np.linalg.inv(within_class_scatter_reg) @ between_class_scatter
        )
        
        # Sort eigenvectors by decreasing eigenvalues
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Select top n_components eigenvectors
        max_components = min(n_classes - 1, n_features)
        actual_components = min(self.n_components, max_components)
        self.W = eigenvectors[:, :actual_components]
        
        return self
        
    def fit_svd(self, X, y):
        """
        Fit LDA using SVD-based approach for better numerical stability,
        especially when dealing with high-dimensional data.
        """
        classes = np.unique(y)
        n_classes = len(classes)
        n_samples, n_features = X.shape
        
        # Calculate class means and frequencies
        class_means = np.zeros((n_classes, n_features))
        class_freqs = np.zeros(n_classes)
        for i, c in enumerate(classes):
            class_mask = (y == c)
            class_freqs[i] = np.sum(class_mask) / n_samples
            class_means[i] = np.mean(X[class_mask], axis=0)
        
        # Calculate global mean
        self.mean = class_freqs @ class_means
        
        def calc_within():
            """Calculate the within-class whitening transform"""
            # Center data by class means
            centered = np.vstack([X[y == c] - class_means[i] for i, c in enumerate(classes)])
            
            # Calculate standard deviation for scaling
            std = np.std(centered, axis=0)
            std[std == 0] = 1.0  # Avoid division by zero
            
            # Scale centered data
            scale = np.sqrt(1.0 / (n_samples - n_classes))
            scaled = scale * (centered / std)
            
            # SVD decomposition
            _, S, Vt = np.linalg.svd(scaled, full_matrices=False)
            
            # Filter small singular values
            rank = np.sum(S > self.tol * S[0])
            
            # Calculate whitening transform
            Vt_scaled = Vt[:rank] / std
            transform = Vt_scaled.T / S[:rank].reshape(1, -1)
            
            return transform, std, rank
        
        def calc_between(whitening_transform):
            """Calculate the between-class projection"""
            # Normalization factor
            factor = 1.0 / (n_classes - 1) if n_classes > 1 else 1.0
            
            # Class weights
            weights = np.sqrt((n_samples * class_freqs) * factor)
            
            # Project weighted class mean differences
            projected = (weights * (class_means - self.mean).T).T @ whitening_transform
            
            # SVD of projected means
            _, S, Vt = np.linalg.svd(projected, full_matrices=False)
            
            # Filter small singular values
            rank = np.sum(S > self.tol * S[0])
            
            return Vt.T[:, :rank], rank
        
        # Calculate whitening transform from within-class data
        whitening_transform, _, within_rank = calc_within()
        
        # Calculate projection from between-class means
        between_proj, between_rank = calc_between(whitening_transform)
        
        # Calculate final projection matrix
        self.W = whitening_transform @ between_proj
        
        # Limit number of components
        max_components = min(n_classes - 1, n_features, between_rank)
        actual_components = min(self.n_components, max_components)
        self.W = self.W[:, :actual_components]
        
        return self

    def transform(self, X):
        return (X - self.mean) @ self.W 

    def get_component(self, idx):
        """
        Get a specific discriminant component (useful for visualization)
        
        Parameters:
        -----------
        idx : int
            Index of the component to retrieve
        
        Returns:
        --------
        component : array
            The requested discriminant component
        """
        if self.W is None:
            raise ValueError("Model has not been fitted yet")
        if idx >= self.W.shape[1]:
            raise IndexError(f"Component index {idx} out of bounds")
        return self.W[:, idx] 