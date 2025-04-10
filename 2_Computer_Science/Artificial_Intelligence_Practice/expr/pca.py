import numpy as np
import matplotlib.pyplot as plt
import os

class PCA:
    """
    Principal Component Analysis implementation
    Reduces dimensionality by projecting data onto principal components
    """
    def __init__(self, n_components=None, output_dir='./output'):
        """
        Initialize PCA with the number of components to keep
        
        Parameters:
        -----------
        n_components : int or None
            Number of principal components to keep.
            If None, all components are kept.
        output_dir : str
            Output directory for visualizations
        """
        self.n_components = n_components
        self.mean = None
        self.components = None
        self.explained_variance = None
        self.explained_variance_ratio = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
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
        # Store original data shape
        n_samples, n_features = X.shape
        
        # Center the data
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
        
        # Calculate covariance matrix
        cov_matrix = np.dot(X_centered.T, X_centered) / (n_samples - 1)
        
        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        
        # Sort eigenvalues and eigenvectors in descending order
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Store explained variance
        self.explained_variance = eigenvalues
        self.explained_variance_ratio = eigenvalues / np.sum(eigenvalues)
        
        # If n_components is not set, use all components
        if self.n_components is None:
            self.n_components = n_features
        
        # Select top n_components eigenvectors
        self.components = eigenvectors[:, :self.n_components]
        
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
        # Check if the model has been fit
        if self.components is None:
            raise ValueError("PCA has not been fit yet")
        
        # Center the data
        X_centered = X - self.mean
        
        # Project the data onto the principal components
        X_transformed = np.dot(X_centered, self.components)
        
        return X_transformed
    
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
        
    def inverse_transform(self, X_transformed):
        """
        Transform data back to its original space
        
        Parameters:
        -----------
        X_transformed : array-like, shape (n_samples, n_components)
            Transformed data
            
        Returns:
        --------
        X_reconstructed : array-like, shape (n_samples, n_features)
            Reconstructed data in original space
        """
        # Check if the model has been fit
        if self.components is None:
            raise ValueError("PCA has not been fit yet")
        
        # Project back to original space
        X_reconstructed = np.dot(X_transformed, self.components.T) + self.mean
        
        return X_reconstructed
    
    def reconstruct_from_n_components(self, X, n_components):
        """
        Reconstruct X using only the first n_components
        
        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Data to transform and reconstruct
        n_components : int
            Number of components to use for reconstruction
            
        Returns:
        --------
        X_reconstructed : array-like, shape (n_samples, n_features)
            Reconstructed data in original space
        """
        # Check if the model has been fit
        if self.components is None:
            raise ValueError("PCA has not been fit yet")
        
        # Center the data
        X_centered = X - self.mean
        
        # Project the data onto all components
        X_transformed = np.dot(X_centered, self.components)
        
        # Keep only the specified number of components
        X_transformed_reduced = np.zeros_like(X_transformed)
        X_transformed_reduced[:, :n_components] = X_transformed[:, :n_components]
        
        # Project back to original space
        X_reconstructed = np.dot(X_transformed_reduced, self.components.T) + self.mean
        
        return X_reconstructed
    
    def plot_explained_variance(self, max_components=None):
        """
        Plot explained variance and cumulative explained variance
        
        Parameters:
        -----------
        max_components : int or None
            Maximum number of components to plot.
            If None, all components are plotted.
        """
        # Check if the model has been fit
        if self.explained_variance is None:
            raise ValueError("PCA has not been fit yet")
        
        # Determine how many components to plot
        if max_components is None:
            max_components = len(self.explained_variance)
        else:
            max_components = min(max_components, len(self.explained_variance))
        
        # Create a range of component indices
        components = range(1, max_components + 1)
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot explained variance
        ax1.bar(components, self.explained_variance_ratio[:max_components], alpha=0.8)
        ax1.set_xlabel('Principal Components')
        ax1.set_ylabel('Explained Variance Ratio')
        ax1.set_title('Explained Variance by Component')
        ax1.set_xticks(components)
        ax1.grid(True)
        
        # Plot cumulative explained variance
        cumulative = np.cumsum(self.explained_variance_ratio[:max_components])
        ax2.step(components, cumulative, where='mid', color='red')
        ax2.axhline(y=0.9, color='k', linestyle='--', alpha=0.5)  # 90% reference line
        ax2.set_xlabel('Principal Components')
        ax2.set_ylabel('Cumulative Explained Variance')
        ax2.set_title('Cumulative Explained Variance')
        ax2.set_xticks(components)
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'pca_explained_variance.png'))
        plt.close()
    
    def plot_2d_projection(self, X, y=None, class_names=None):
        """
        Plot 2D projection of the data using the first two principal components
        
        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Data to transform and plot
        y : array-like, shape (n_samples,) or None
            Labels for coloring the points
        class_names : list of str or None
            Names of the classes for the legend
        """
        # Check if the model has been fit
        if self.components is None:
            raise ValueError("PCA has not been fit yet")
        
        # Transform the data
        X_transformed = self.transform(X)
        
        # We need at least 2 components for a 2D plot
        if X_transformed.shape[1] < 2:
            raise ValueError("Need at least 2 components for a 2D plot")
        
        plt.figure(figsize=(10, 8))
        
        # If labels are provided, color the points accordingly
        if y is not None:
            unique_labels = np.unique(y)
            for i, label in enumerate(unique_labels):
                indices = np.where(y == label)[0]
                label_name = class_names[i] if class_names is not None else f"Class {label}"
                plt.scatter(X_transformed[indices, 0], X_transformed[indices, 1], 
                           alpha=0.7, label=label_name)
            plt.legend()
        else:
            plt.scatter(X_transformed[:, 0], X_transformed[:, 1], alpha=0.7)
        
        plt.xlabel(f'Principal Component 1 ({self.explained_variance_ratio[0]:.2%})')
        plt.ylabel(f'Principal Component 2 ({self.explained_variance_ratio[1]:.2%})')
        plt.title('2D PCA Projection')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'pca_2d_projection.png'))
        plt.close()
    
    def visualize_components(self, n_components=10, image_shape=None):
        """
        Visualize the principal components as images
        
        Parameters:
        -----------
        n_components : int
            Number of components to visualize
        image_shape : tuple (height, width) or None
            Shape of the original images.
            If None, the components are visualized as 1D plots.
        """
        # Check if the model has been fit
        if self.components is None:
            raise ValueError("PCA has not been fit yet")
        
        # Determine how many components to visualize
        n_to_visualize = min(n_components, self.components.shape[1])
        
        if image_shape is not None:
            # Visualize as images (for image data)
            n_cols = min(5, n_to_visualize)
            n_rows = (n_to_visualize + n_cols - 1) // n_cols
            
            plt.figure(figsize=(12, 2 * n_rows))
            
            for i in range(n_to_visualize):
                component = self.components[:, i].reshape(image_shape)
                plt.subplot(n_rows, n_cols, i + 1)
                plt.imshow(component, cmap='viridis')
                plt.title(f'PC {i+1}')
                plt.axis('off')
                
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'pca_components_as_images.png'))
            plt.close()
        else:
            # Visualize as 1D plots (for non-image data)
            n_cols = min(2, n_to_visualize)
            n_rows = (n_to_visualize + n_cols - 1) // n_cols
            
            plt.figure(figsize=(12, 3 * n_rows))
            
            for i in range(n_to_visualize):
                plt.subplot(n_rows, n_cols, i + 1)
                plt.plot(self.components[:, i])
                plt.title(f'Principal Component {i+1}')
                plt.grid(True)
                
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'pca_components_as_plots.png'))
            plt.close() 