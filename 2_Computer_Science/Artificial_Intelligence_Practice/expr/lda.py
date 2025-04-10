import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt
import os
import joblib

class LDADimensionReducer:
    """Linear Discriminant Analysis for dimensionality reduction"""
    
    def __init__(self, output_dir='./output'):
        """Initialize LDA dimension reducer"""
        self.model = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def fit(self, X, y, n_components=None, solver='svd'):
        """
        Fit LDA model for dimensionality reduction
        
        Parameters:
        -----------
        X : array-like
            Training data features
        y : array-like
            Training data labels
        n_components : int, optional
            Number of components for dimensionality reduction
        solver : str, default='svd'
            Solver to use ('svd', 'lsqr', or 'eigen')
            
        Returns:
        --------
        self : object
            Returns self for method chaining
        """
        print(f"\nFitting LDA for dimensionality reduction with solver={solver}...")
        
        # LDA components are limited by number of classes - 1
        if n_components is not None:
            n_components = min(n_components, len(np.unique(y)) - 1)
            print(f"Using {n_components} components for LDA")
            
        self.model = LinearDiscriminantAnalysis(n_components=n_components, solver=solver)
        
        # Fit model
        self.model.fit(X, y)
        
        # Calculate explained variance ratio
        if hasattr(self.model, 'explained_variance_ratio_'):
            explained_variance = self.model.explained_variance_ratio_
            print(f"Explained variance ratio: {explained_variance}")
            
            # Visualize explained variance
            plt.figure(figsize=(10, 6))
            plt.bar(range(1, len(explained_variance) + 1), explained_variance, alpha=0.7)
            plt.step(range(1, len(explained_variance) + 1), np.cumsum(explained_variance), where='mid', color='red')
            plt.xlabel('LDA Components')
            plt.ylabel('Explained Variance Ratio')
            plt.title('Explained Variance by LDA Components')
            plt.savefig(os.path.join(self.output_dir, 'lda_explained_variance.png'))
            plt.close()
        
        return self
    
    def transform(self, X):
        """
        Transform data to lower-dimensional space using LDA
        
        Parameters:
        -----------
        X : array-like
            Data to transform
            
        Returns:
        --------
        X_transformed : array-like
            Transformed data
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
            
        return self.model.transform(X)
    
    def fit_transform(self, X, y, n_components=None, solver='svd'):
        """
        Fit LDA model and transform data in one step
        
        Parameters:
        -----------
        X : array-like
            Training data features
        y : array-like
            Training data labels
        n_components : int, optional
            Number of components for dimensionality reduction
        solver : str, default='svd'
            Solver to use ('svd', 'lsqr', or 'eigen')
            
        Returns:
        --------
        X_transformed : array-like
            Transformed data
        """
        self.fit(X, y, n_components, solver)
        return self.transform(X)
    
    def visualize_projection(self, X, y, class_names, max_components=2):
        """
        Visualize data projection in LDA space (for up to 2 components)
        
        Parameters:
        -----------
        X : array-like
            Data to transform and visualize
        y : array-like
            Labels for coloring the points
        class_names : list of str
            Names of the classes for the legend
        max_components : int, default=2
            Maximum number of components to visualize
        """
        if self.model is None:
            raise ValueError("Model has not been fitted yet")
            
        # Transform data
        X_lda = self.transform(X)
        
        # We can only visualize 1 or 2 components
        actual_components = min(X_lda.shape[1], max_components)
        
        if actual_components == 1:
            # 1D visualization
            plt.figure(figsize=(12, 6))
            for i, label in enumerate(np.unique(y)):
                indices = np.where(y == label)[0]
                plt.scatter(X_lda[indices], np.zeros_like(X_lda[indices]), alpha=0.7, label=class_names[i])
            plt.xlabel('LD1')
            plt.title('LDA Projection (1D)')
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'lda_projection_1d.png'))
            plt.close()
            
        elif actual_components >= 2:
            # 2D visualization
            plt.figure(figsize=(12, 10))
            for i, label in enumerate(np.unique(y)):
                indices = np.where(y == label)[0]
                plt.scatter(X_lda[indices, 0], X_lda[indices, 1], alpha=0.7, label=class_names[i])
            plt.xlabel('LD1')
            plt.ylabel('LD2')
            plt.title('LDA Projection (2D)')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'lda_projection_2d.png'))
            plt.close()
    
    def save_model(self, filename='lda_model.pkl'):
        """Save the fitted model"""
        if self.model is None:
            raise ValueError("No model to save")
            
        model_path = os.path.join(self.output_dir, filename)
        joblib.dump(self.model, model_path)
        print(f"\nModel saved to {model_path}")
        
        return model_path
    
    def load_model(self, model_path):
        """Load a previously fitted model"""
        self.model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
        
        return self.model 