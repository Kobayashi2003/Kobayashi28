import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

class LDAdimReducer:
    def __init__(self, n_components=None):
        """
        Initialize LDA dimension reducer
        
        Args:
            n_components: Number of components to keep (default: min(n_classes-1, n_features))
        """
        self.n_components = n_components
        
        # Ensure n_components is at least 1 if specified
        if isinstance(n_components, (int, float)) and n_components <= 0:
            print(f"Warning: n_components={n_components} is invalid for LDA. Setting to None.")
            self.n_components = None
        
        self.lda = LinearDiscriminantAnalysis(n_components=self.n_components)
        self.is_fitted = False
        
    def fit(self, X, y):
        """
        Fit LDA model to data
        
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
        
        # For LDA, n_components must be between 1 and min(n_features, n_classes-1)
        n_classes = len(np.unique(y))
        n_features = X_reshaped.shape[1]
        max_components = min(n_features, n_classes - 1)
        
        # If n_components is specified as a float (e.g., 0.95 for PCA), 
        # convert to an integer for LDA
        if isinstance(self.n_components, float) and 0 < self.n_components < 1:
            print(f"Warning: n_components as a fraction ({self.n_components}) is not supported for LDA. Using maximum value.")
            self.n_components = max_components
            # Recreate the LDA object with the corrected n_components
            self.lda = LinearDiscriminantAnalysis(n_components=self.n_components)
        elif isinstance(self.n_components, int) and self.n_components > max_components:
            print(f"Warning: n_components={self.n_components} exceeds maximum allowed ({max_components}). Adjusting.")
            self.n_components = max_components
            # Recreate the LDA object with the corrected n_components
            self.lda = LinearDiscriminantAnalysis(n_components=self.n_components)
        
        print(f"Using LDA with n_components={self.n_components} (max possible: {max_components})")
        self.lda.fit(X_reshaped, y)
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
            raise ValueError("LDA model must be fitted before transforming data")
        
        # Reshape image data to 2D if needed
        if len(X.shape) > 2:
            n_samples = X.shape[0]
            X_reshaped = X.reshape(n_samples, -1)
        else:
            X_reshaped = X
            
        return self.lda.transform(X_reshaped)
        
    def fit_transform(self, X, y):
        """
        Fit LDA model and apply dimension reduction in one step
        
        Args:
            X: Input data of shape (n_samples, n_features)
            y: Target labels of shape (n_samples,)
            
        Returns:
            X_transformed: Transformed data
        """
        return self.fit(X, y).transform(X)
        
    def predict(self, X):
        """
        Predict class labels for samples in X
        
        Args:
            X: Input data of shape (n_samples, n_features)
            
        Returns:
            y_pred: Predicted class labels
        """
        if not self.is_fitted:
            raise ValueError("LDA model must be fitted before predicting")
        
        # Reshape image data to 2D if needed
        if len(X.shape) > 2:
            n_samples = X.shape[0]
            X_reshaped = X.reshape(n_samples, -1)
        else:
            X_reshaped = X
            
        return self.lda.predict(X_reshaped)
