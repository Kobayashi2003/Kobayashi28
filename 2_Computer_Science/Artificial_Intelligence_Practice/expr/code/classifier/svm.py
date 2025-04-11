# Standard library imports
import os
import time

# Third-party imports - data analysis and scientific computing
import numpy as np

# Third-party imports - machine learning
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Third-party imports - visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Third-party imports - utilities
import joblib

class SVMClassifier:
    """Support Vector Machine classifier implementation"""
    
    def __init__(self, output_dir='./output/svm'):
        """
        Initialize SVM classifier
        
        Parameters:
        -----------
        output_dir : str
            Output directory for results
        """
        self.model = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def train_standard(self, X_train, y_train, X_valid=None, y_valid=None, 
                      C=1.0, kernel='rbf', gamma='scale'):
        """
        Train a standard SVM classifier with specified parameters
        
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
        C : float
            Regularization parameter
        kernel : str
            Kernel type ('linear', 'poly', 'rbf', 'sigmoid')
        gamma : str or float
            Kernel coefficient for 'rbf', 'poly' and 'sigmoid' kernels
            
        Returns:
        --------
        self : SVMClassifier
            Trained classifier
        """
        print(f"\nTraining standard SVM with kernel={kernel}, C={C}, gamma={gamma}")
        start_time = time.time()
        
        # Create and train SVM model
        self.model = SVC(C=C, kernel=kernel, gamma=gamma, probability=True)
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
        Train SVM using grid search for hyperparameter optimization
        
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
        self : SVMClassifier
            Trained classifier
        """
        print("\nTraining SVM with grid search")
        
        # Default parameter grid if not provided
        if param_grid is None:
            param_grid = {
                'C': [0.1, 1, 10, 100],
                'kernel': ['linear', 'rbf'],
                'gamma': ['scale', 'auto', 0.1, 0.01]
            }
        
        # Create and fit grid search
        svm = SVC(probability=True)
        grid_search = GridSearchCV(svm, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
        
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
    
    def train_ovr(self, X_train, y_train, X_valid=None, y_valid=None, 
                 C=1.0, kernel='rbf', gamma='scale'):
        """
        Train a One-vs-Rest SVM classifier
        
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
        C : float
            Regularization parameter
        kernel : str
            Kernel type ('linear', 'poly', 'rbf', 'sigmoid')
        gamma : str or float
            Kernel coefficient for 'rbf', 'poly' and 'sigmoid' kernels
            
        Returns:
        --------
        self : SVMClassifier
            Trained classifier
        """
        print(f"\nTraining One-vs-Rest SVM with kernel={kernel}, C={C}, gamma={gamma}")
        start_time = time.time()
        
        # Create and train OVR SVM model
        base_svm = SVC(C=C, kernel=kernel, gamma=gamma, probability=True)
        self.model = OneVsRestClassifier(base_svm)
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
    
    def train_ovo(self, X_train, y_train, X_valid=None, y_valid=None,
                 C=1.0, kernel='rbf', gamma='scale'):
        """
        Train a One-vs-One SVM classifier
        
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
        C : float
            Regularization parameter
        kernel : str
            Kernel type ('linear', 'poly', 'rbf', 'sigmoid')
        gamma : str or float
            Kernel coefficient for 'rbf', 'poly' and 'sigmoid' kernels
            
        Returns:
        --------
        self : SVMClassifier
            Trained classifier
        """
        print(f"\nTraining One-vs-One SVM with kernel={kernel}, C={C}, gamma={gamma}")
        start_time = time.time()
        
        # Create and train OVO SVM model
        base_svm = SVC(C=C, kernel=kernel, gamma=gamma, probability=True)
        self.model = OneVsOneClassifier(base_svm)
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
    
    def train_ensemble(self, X_train, y_train, X_valid=None, y_valid=None):
        """
        Train an ensemble of different SVM models
        
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
            
        Returns:
        --------
        self : SVMClassifier
            Trained classifier
        """
        from sklearn.ensemble import VotingClassifier
        
        print("\nTraining SVM ensemble with different kernels")
        
        # Create different SVM classifiers
        estimators = [
            ('linear', SVC(kernel='linear', probability=True)),
            ('rbf', SVC(kernel='rbf', probability=True)),
            ('poly', SVC(kernel='poly', degree=3, probability=True))
        ]
        
        # Create and train ensemble
        self.model = VotingClassifier(estimators, voting='soft')
        
        start_time = time.time()
        self.model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        print(f"Ensemble training completed in {training_time:.2f} seconds")
        
        # Evaluate on training set
        train_accuracy = self.model.score(X_train, y_train)
        print(f"Training accuracy: {train_accuracy:.4f}")
        
        # Evaluate on validation set if provided
        if X_valid is not None and y_valid is not None:
            valid_accuracy = self.model.score(X_valid, y_valid)
            print(f"Validation accuracy: {valid_accuracy:.4f}")
        
        return self
    
    def evaluate(self, X_test, y_test, class_names, filename_suffix=''):
        """
        Evaluate model on test data and generate reports
        
        Parameters:
        -----------
        X_test : array-like
            Test features
        y_test : array-like
            Test labels
        class_names : list
            List of class names
        filename_suffix : str, optional
            Suffix to add to output filenames
            
        Returns:
        --------
        test_accuracy : float
            Test accuracy
        y_pred : array-like
            Predicted labels
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        # Predict on test set
        y_pred = self.model.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nTest set accuracy = {test_accuracy:.4f}")
        
        # Generate classification report
        class_report = classification_report(y_test, y_pred, target_names=class_names)
        print("\nClassification Report:")
        print(class_report)
        
        # Save classification report
        report_file = f'classification_report{filename_suffix}.txt'
        with open(os.path.join(self.output_dir, report_file), 'w') as f:
            f.write(f"Test accuracy: {test_accuracy:.4f}\n\n")
            f.write(class_report)
        
        # Generate confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.xlabel('Predicted label')
        plt.ylabel('True label')
        plt.title('Confusion Matrix')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'confusion_matrix{filename_suffix}.png'))
        plt.close()
        
        # Calculate and plot per-class accuracy
        class_accuracy = np.diag(cm) / np.sum(cm, axis=1)
        plt.figure(figsize=(12, 6))
        plt.bar(class_names, class_accuracy)
        plt.xlabel('Class')
        plt.ylabel('Accuracy')
        plt.title('Classification Accuracy by Class')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'class_accuracy{filename_suffix}.png'))
        plt.close()
        
        # If model supports probabilities, plot decision confidence
        if hasattr(self.model, 'predict_proba'):
            try:
                y_proba = self.model.predict_proba(X_test)
                confidences = [proba.max() for proba in y_proba]
                
                plt.figure(figsize=(10, 6))
                plt.hist(confidences, bins=20, alpha=0.7)
                plt.xlabel('Confidence (max probability)')
                plt.ylabel('Frequency')
                plt.title('Distribution of Decision Confidence')
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_dir, f'decision_confidence{filename_suffix}.png'))
                plt.close()
            except:
                pass
        
        return test_accuracy, y_pred
    
    def save_model(self, filename='svm_model.pkl'):
        """Save the trained model"""
        if self.model is None:
            raise ValueError("No model to save")
            
        model_path = os.path.join(self.output_dir, filename)
        joblib.dump(self.model, model_path)
        print(f"\nModel saved to {model_path}")
        
        return model_path
    
    def load_model(self, model_path):
        """Load a previously trained model"""
        self.model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
        
        return self.model
    
    def predict(self, X):
        """Make predictions using the trained model"""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Predict class probabilities using the trained model"""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X)
        else:
            raise AttributeError("Model does not support probability predictions")
    
    def _plot_param_comparison(self, grid_search):
        """Plot parameter comparison from grid search results"""
        results = grid_search.cv_results_
        
        # Extract unique parameter values
        params = grid_search.param_grid
        
        # If C parameter was varied
        if 'C' in params and len(params['C']) > 1:
            plt.figure(figsize=(10, 6))
            for kernel in params.get('kernel', ['rbf']):
                kernel_mask = np.array([p['kernel'] == kernel for p in results['params']])
                
                # For each gamma value
                for gamma in params.get('gamma', ['scale']):
                    gamma_mask = np.array([p.get('gamma', 'scale') == gamma 
                                         for p in results['params']])
                    
                    # Get results for this kernel and gamma
                    mask = kernel_mask & gamma_mask
                    if not any(mask):
                        continue
                    
                    # Extract C values and corresponding scores
                    c_values = [p['C'] for p in np.array(results['params'])[mask]]
                    scores = results['mean_test_score'][mask]
                    
                    # Sort by C value
                    c_indices = np.argsort(c_values)
                    c_values = np.array(c_values)[c_indices]
                    scores = np.array(scores)[c_indices]
                    
                    # Plot scores vs C for this kernel and gamma
                    plt.plot(c_values, scores, 'o-', 
                            label=f'{kernel}, gamma={gamma}')
            
            plt.xlabel('C value (log scale)')
            plt.xscale('log')
            plt.ylabel('Cross-validation accuracy')
            plt.title('SVM Accuracy for Different C Values')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'c_parameter_comparison.png'))
            plt.close()
        
        # If gamma parameter was varied
        if 'gamma' in params and len(params['gamma']) > 1:
            numerical_gammas = []
            for g in params['gamma']:
                if g == 'scale':
                    numerical_gammas.append(0.1)  # Arbitrary value for visualization
                elif g == 'auto':
                    numerical_gammas.append(0.05)  # Arbitrary value for visualization
                else:
                    numerical_gammas.append(float(g))
            
            plt.figure(figsize=(10, 6))
            for kernel in params.get('kernel', ['rbf']):
                if kernel not in ['rbf', 'poly', 'sigmoid']:
                    continue  # gamma only relevant for certain kernels
                    
                kernel_mask = np.array([p['kernel'] == kernel for p in results['params']])
                
                # For each C value
                for c in params.get('C', [1.0]):
                    c_mask = np.array([p.get('C', 1.0) == c for p in results['params']])
                    
                    # Get results for this kernel and C
                    mask = kernel_mask & c_mask
                    if not any(mask):
                        continue
                    
                    # Extract gamma values and corresponding scores
                    gamma_values = [p['gamma'] if p['gamma'] not in ['scale', 'auto'] 
                                   else ('scale' if p['gamma'] == 'scale' else 'auto')
                                   for p in np.array(results['params'])[mask]]
                    scores = results['mean_test_score'][mask]
                    
                    # Plot scores vs gamma for this kernel and C
                    plt.plot(range(len(gamma_values)), scores, 'o-', 
                            label=f'{kernel}, C={c}')
            
            plt.xlabel('Gamma value')
            plt.xticks(range(len(params['gamma'])), params['gamma'])
            plt.ylabel('Cross-validation accuracy')
            plt.title('SVM Accuracy for Different Gamma Values')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'gamma_parameter_comparison.png'))
            plt.close()
        
        # If kernel parameter was varied
        if 'kernel' in params and len(params['kernel']) > 1:
            plt.figure(figsize=(10, 6))
            kernel_scores = {}
            
            for kernel in params['kernel']:
                kernel_mask = np.array([p['kernel'] == kernel for p in results['params']])
                kernel_scores[kernel] = np.mean(results['mean_test_score'][kernel_mask])
            
            plt.bar(kernel_scores.keys(), kernel_scores.values())
            plt.xlabel('Kernel')
            plt.ylabel('Average cross-validation accuracy')
            plt.title('SVM Accuracy for Different Kernels')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'kernel_comparison.png'))
            plt.close()
