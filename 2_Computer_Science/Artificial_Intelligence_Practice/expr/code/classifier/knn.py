# Standard library imports
import os
import time

# Third-party imports - data analysis and scientific computing
import numpy as np
import pandas as pd

# Third-party imports - machine learning
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Third-party imports - visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Third-party imports - utilities
import joblib

class KNNClassifier:
    """K-Nearest Neighbors classifier implementation"""
    
    def __init__(self, output_dir='./output/knn'):
        """
        Initialize KNN classifier
        
        Parameters:
        -----------
        output_dir : str
            Output directory for results
        """
        self.model = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def train_standard(self, X_train, y_train, X_valid=None, y_valid=None, 
                      n_neighbors=5, weights='uniform', algorithm='auto', p=2):
        """
        Train a standard KNN classifier with specified parameters
        
        Parameters:
        -----------
        X_train : array-like
            Training features
        y_train : array-like
            Training labels
        X_valid : array-like, optional
            Validation features
        y_valid : array-like, optional
            Validation labels
        n_neighbors : int
            Number of neighbors
        weights : str
            Weight function ('uniform' or 'distance')
        algorithm : str
            Algorithm to compute nearest neighbors ('auto', 'ball_tree', 'kd_tree', or 'brute')
        p : int
            Power parameter for Minkowski metric (p=1 for Manhattan, p=2 for Euclidean)
            
        Returns:
        --------
        self : KNNClassifier
            Trained classifier
        """
        print(f"\nTraining standard KNN with n_neighbors={n_neighbors}, weights={weights}, algorithm={algorithm}, p={p}")
        start_time = time.time()
        
        # Create and train KNN model
        self.model = KNeighborsClassifier(
            n_neighbors=n_neighbors, 
            weights=weights, 
            algorithm=algorithm, 
            p=p
        )
        self.model.fit(X_train, y_train)
        
        training_time = time.time() - start_time
        print(f"Training completed in {training_time:.2f} seconds")
        
        # Evaluate on training set
        train_accuracy = self.model.score(X_train, y_train)
        print(f"Training accuracy: {train_accuracy:.4f}")
        
        # Evaluate on validation set if provided
        if X_valid is not None and y_valid is not None:
            valid_accuracy = self.model.score(X_valid, y_valid)
            print(f"Validation accuracy: {valid_accuracy:.4f}")
        
        return self
    
    def train_grid_search(self, X_train, y_train, param_grid=None):
        """
        Train KNN using grid search for hyperparameter optimization
        
        Parameters:
        -----------
        X_train : array-like
            Training features
        y_train : array-like
            Training labels
        param_grid : dict, optional
            Grid of parameters to search over
            
        Returns:
        --------
        self : KNNClassifier
            Trained classifier
        """
        print("\nTraining KNN with grid search")
        
        # Default parameter grid if not provided
        if param_grid is None:
            param_grid = {
                'n_neighbors': [3, 5, 7, 9, 11, 13],
                'weights': ['uniform', 'distance'],
                'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                'p': [1, 2]
            }
        
        # Create and fit grid search
        knn = KNeighborsClassifier()
        grid_search = GridSearchCV(knn, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
        
        start_time = time.time()
        grid_search.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        # Output best parameters
        print(f"Grid search completed in {training_time:.2f} seconds")
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best cross-validation accuracy: {grid_search.best_score_:.4f}")
        
        # Set the best model
        self.model = grid_search.best_estimator_
        
        # Save grid search results
        with open(os.path.join(self.output_dir, 'grid_search_results.txt'), 'w') as f:
            f.write(f"Best parameters: {grid_search.best_params_}\n")
            f.write(f"Best validation accuracy: {grid_search.best_score_:.4f}\n\n")
            f.write("All results:\n")
            for i, params in enumerate(grid_search.cv_results_['params']):
                f.write(f"{params}: {grid_search.cv_results_['mean_test_score'][i]:.4f}\n")
        
        # Plot parameter comparison
        self._plot_param_comparison(grid_search)
        
        return self
    
    def evaluate(self, X_test, y_test, class_names, filename_suffix=''):
        """
        Evaluate the model on test data
        
        Parameters:
        -----------
        X_test : array-like
            Test features
        y_test : array-like
            Test labels
        class_names : list
            List of class names
        filename_suffix : str, optional
            Suffix for output filenames
            
        Returns:
        --------
        accuracy : float
            Test accuracy
        """
        # Use non-interactive backend to avoid Tkinter thread errors
        import matplotlib
        matplotlib.use('Agg')  # 使用Agg后端，不依赖于Tkinter
        
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        
        print("\nEvaluating KNN classifier on test data")
        
        # Make predictions
        start_time = time.time()
        y_pred = self.model.predict(X_test)
        inference_time = time.time() - start_time
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Test accuracy: {accuracy:.4f}")
        print(f"Inference time for {len(X_test)} samples: {inference_time:.2f} seconds")
        print(f"Average inference time per sample: {inference_time/len(X_test)*1000:.2f} ms")
        
        # Generate classification report
        report = classification_report(y_test, y_pred, target_names=class_names, digits=4)
        print("\nClassification Report:")
        print(report)
        
        # Save classification report
        with open(os.path.join(self.output_dir, f'classification_report{filename_suffix}.txt'), 'w') as f:
            f.write(f"Test accuracy: {accuracy:.4f}\n")
            f.write(f"Inference time: {inference_time:.2f} seconds\n\n")
            f.write(report)
        
        # Create and plot confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'confusion_matrix{filename_suffix}.png'))
        plt.close('all')  # 确保所有图形被关闭
        
        return accuracy
    
    def save_model(self, filename='knn_model.pkl'):
        """
        Save the model to disk
        
        Parameters:
        -----------
        filename : str
            Filename to save model
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        
        model_path = os.path.join(self.output_dir, filename)
        joblib.dump(self.model, model_path)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path):
        """Load a saved model from disk"""
        self.model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
        return self
    
    def predict(self, X):
        """Make predictions for samples in X"""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Return probability estimates for samples in X
        
        Note: KNN only supports probability predictions when weights='distance'
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        # Check if model supports probability predictions
        if not hasattr(self.model, 'predict_proba'):
            raise ValueError("This KNN model does not support probability predictions")
            
        return self.model.predict_proba(X)
    
    def _plot_param_comparison(self, grid_search):
        """
        Plot comparison of different parameters from grid search
        
        Parameters:
        -----------
        grid_search : GridSearchCV
            Fitted grid search object
        """
        # Use non-interactive backend to avoid Tkinter thread errors
        import matplotlib
        matplotlib.use('Agg')  # 使用Agg后端，不依赖于Tkinter
        
        # Extract results
        results = pd.DataFrame(grid_search.cv_results_)
        
        # For each parameter, create a plot showing its effect on accuracy
        params = list(grid_search.param_grid.keys())
        
        for param in params:
            if len(grid_search.param_grid[param]) > 1:
                plt.figure(figsize=(10, 6))
                # Group by parameter and calculate mean accuracy
                grouped = results.groupby(f'param_{param}')['mean_test_score'].mean()
                
                # Convert to numeric if possible for proper ordering
                try:
                    param_values = [float(x) for x in grouped.index]
                    sorted_idx = np.argsort(param_values)
                    param_values = [param_values[i] for i in sorted_idx]
                    accuracy_values = [grouped.iloc[i] for i in sorted_idx]
                except (ValueError, TypeError):
                    param_values = grouped.index
                    accuracy_values = grouped.values
                
                plt.bar([str(x) for x in param_values], accuracy_values)
                plt.xlabel(param)
                plt.ylabel('Mean CV Accuracy')
                plt.title(f'Effect of {param} on Accuracy')
                plt.ylim(0.5, 1.0)  # Adjust as needed
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_dir, f'param_comparison_{param}.png'))
                plt.close('all')  # 确保所有图形被关闭
