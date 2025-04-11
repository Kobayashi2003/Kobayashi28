import numpy as np
import matplotlib
matplotlib.use('Agg')  # 设置为非交互式后端
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA as SklearnPCA
import seaborn as sns

class PCA:
    """
    PCA implementation for dimensionality reduction
    """
    
    def __init__(self, n_components=None, output_dir='./output/pca'):
        """
        Initialize PCA for dimensionality reduction
        
        Parameters:
        -----------
        n_components : int, optional
            Number of components to keep
        output_dir : str
            Directory to save output plots
        """
        self.n_components = n_components
        self.model = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def fit_transform(self, X):
        """
        Fit PCA model and transform data
        
        Parameters:
        -----------
        X : array-like
            Input features
            
        Returns:
        --------
        X_transformed : array-like
            Transformed features
        """
        # Create and fit the PCA model
        self.model = SklearnPCA(n_components=self.n_components)
        X_transformed = self.model.fit_transform(X)
        
        # Store explained variance
        self.explained_variance = self.model.explained_variance_
        self.explained_variance_ratio = self.model.explained_variance_ratio_
        self.components = self.model.components_
        
        return X_transformed
    
    def transform(self, X):
        """
        Transform data using fitted PCA model
        
        Parameters:
        -----------
        X : array-like
            Input features
            
        Returns:
        --------
        X_transformed : array-like
            Transformed features
        """
        if self.model is None:
            raise ValueError("PCA model has not been fitted yet")
            
        return self.model.transform(X)
    
    def inverse_transform(self, X_transformed):
        """
        Transform data back to original space
        
        Parameters:
        -----------
        X_transformed : array-like
            Transformed features
            
        Returns:
        --------
        X_reconstructed : array-like
            Reconstructed features in original space
        """
        if self.model is None:
            raise ValueError("PCA model has not been fitted yet")
            
        return self.model.inverse_transform(X_transformed)
    
    def plot_explained_variance(self, max_components=None):
        """
        Plot explained variance by principal components
        
        Parameters:
        -----------
        max_components : int, optional
            Maximum number of components to plot
        """
        if self.model is None:
            raise ValueError("PCA model has not been fitted yet")
            
        # Determine number of components to plot
        if max_components is None:
            max_components = len(self.explained_variance_ratio)
        else:
            max_components = min(max_components, len(self.explained_variance_ratio))
            
        # Calculate cumulative explained variance
        cum_var = np.cumsum(self.explained_variance_ratio[:max_components])
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.bar(range(1, max_components + 1), 
               self.explained_variance_ratio[:max_components], alpha=0.7, 
               label='Individual explained variance')
        plt.step(range(1, max_components + 1), cum_var, where='mid', 
                label='Cumulative explained variance', color='red')
        plt.axhline(y=0.95, color='k', linestyle='--', alpha=0.7, label='95% threshold')
        plt.xlabel('Number of components')
        plt.ylabel('Explained variance ratio')
        plt.title('Explained Variance by Principal Components')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'pca_explained_variance.png'))
        plt.close('all')  # 确保关闭所有图形
    
    def plot_2d_projection(self, X, y=None, class_names=None):
        """
        Plot 2D projection of data
        
        Parameters:
        -----------
        X : array-like
            Input features
        y : array-like, optional
            Target labels
        class_names : list, optional
            List of class names
        """
        if self.model is None:
            self.fit_transform(X)
            
        # Transform data and get first two principal components
        X_pca = self.transform(X)
        
        # Create figure
        plt.figure(figsize=(12, 10))
        
        # If labels are provided, create a scatter plot with class colors
        if y is not None:
            unique_classes = np.unique(y)
            
            # Create scatter plot
            scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='tab10', alpha=0.7)
            
            # Add legend with class names if provided
            if class_names is not None and len(class_names) <= 10:
                handles, _ = scatter.legend_elements()
                plt.legend(handles, class_names, title="Classes")
        else:
            # Without labels, create a simple scatter plot
            plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.7)
        
        # Add title and labels
        plt.title('PCA: First two principal components')
        plt.xlabel(f'Principal Component 1 ({self.explained_variance_ratio[0]:.2%} variance)')
        plt.ylabel(f'Principal Component 2 ({self.explained_variance_ratio[1]:.2%} variance)')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'pca_2d_projection.png'))
        plt.close('all')  # 确保关闭所有图形
