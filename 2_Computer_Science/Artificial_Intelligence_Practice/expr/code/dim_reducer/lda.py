import numpy as np
import matplotlib
matplotlib.use('Agg')  # 设置为非交互式后端
import matplotlib.pyplot as plt
import os
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import LabelEncoder
import seaborn as sns

class LDADimensionReducer:
    """
    Linear Discriminant Analysis for dimensionality reduction
    """
    
    def __init__(self, output_dir='./output/lda'):
        """
        Initialize LDA for dimensionality reduction
        
        Parameters:
        -----------
        output_dir : str
            Directory to save output plots
        """
        self.model = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def fit_transform(self, X, y, n_components=None):
        """
        Fit LDA model and transform data
        
        Parameters:
        -----------
        X : array-like
            Input features
        y : array-like
            Target labels
        n_components : int, optional
            Number of components to keep
            
        Returns:
        --------
        X_transformed : array-like
            Transformed features
        """
        # Default n_components is min(n_classes - 1, n_features)
        if n_components is None:
            n_components = min(len(np.unique(y)) - 1, X.shape[1])
            
        # Create and fit the LDA model
        self.model = LinearDiscriminantAnalysis(n_components=n_components)
        X_transformed = self.model.fit_transform(X, y)
        
        # Save explained variance
        self.explained_variance_ratio = self.model.explained_variance_ratio_
        
        # Plot explained variance
        self._plot_explained_variance()
        
        return X_transformed
    
    def transform(self, X):
        """
        Transform data using fitted LDA model
        
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
            raise ValueError("LDA model has not been fitted yet")
            
        return self.model.transform(X)
    
    def _plot_explained_variance(self):
        """Plot explained variance ratio"""
        if hasattr(self, 'explained_variance_ratio'):
            cum_var = np.cumsum(self.explained_variance_ratio)
            
            plt.figure(figsize=(10, 6))
            plt.bar(range(1, len(self.explained_variance_ratio) + 1), 
                   self.explained_variance_ratio, alpha=0.7, label='Individual explained variance')
            plt.step(range(1, len(cum_var) + 1), cum_var, where='mid', 
                    label='Cumulative explained variance', color='red')
            plt.axhline(y=0.95, color='k', linestyle='--', alpha=0.7, label='95% threshold')
            plt.xlabel('Number of components')
            plt.ylabel('Explained variance ratio')
            plt.title('Explained Variance by LDA Components')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'lda_explained_variance.png'))
            plt.close('all')  # 确保关闭所有图形
    
    def visualize_projection(self, X, y, class_names):
        """
        Visualize LDA projection in 2D
        
        Parameters:
        -----------
        X : array-like
            Input features
        y : array-like
            Target labels
        class_names : list
            List of class names
        """
        if self.model is None:
            raise ValueError("LDA model has not been fitted yet")
            
        # Ensure we have at least 2 components for 2D projection
        n_components = min(2, self.model.n_components)
        
        if n_components < 2:
            print("Cannot create 2D projection, not enough components")
            return
            
        # Transform data
        X_lda = self.model.transform(X)[:, :2]  # Get first two components
        
        # Create encoder to handle string labels
        le = LabelEncoder().fit(y)
        y_encoded = le.transform(y)
        
        # Create plot
        plt.figure(figsize=(12, 10))
        scatter = plt.scatter(X_lda[:, 0], X_lda[:, 1], c=y_encoded, cmap='tab10', alpha=0.7)
        
        # Add class labels to legend
        if len(class_names) <= 10:  # Only show legend if not too many classes
            handles, _ = scatter.legend_elements()
            plt.legend(handles, class_names, title="Classes")
        
        # Add title and labels
        plt.title('LDA Projection of the Dataset')
        plt.xlabel('LD1')
        plt.ylabel('LD2')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'lda_projection.png'))
        plt.close('all')  # 确保关闭所有图形
