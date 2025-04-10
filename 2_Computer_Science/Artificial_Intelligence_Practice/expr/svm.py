import numpy as np
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib

class SVMClassifier:
    """Support Vector Machine classifier with multiple strategies"""
    
    def __init__(self, output_dir='./output'):
        """Initialize SVM classifier"""
        self.model = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def train_basic(self, X_train, y_train, kernel='rbf', C=1.0, gamma='scale'):
        """
        Train a basic SVM model with specified parameters
        
        Parameters:
        -----------
        X_train : array-like
            Training data features
        y_train : array-like
            Training data labels
        kernel : str, default='rbf'
            Kernel type to be used in the algorithm
        C : float, default=1.0
            Regularization parameter
        gamma : str or float, default='scale'
            Kernel coefficient for 'rbf', 'poly' and 'sigmoid'
        """
        print(f"\nTraining basic SVM with kernel={kernel}, C={C}, gamma={gamma}...")
        
        # Create and train SVM classifier
        self.model = SVC(kernel=kernel, C=C, gamma=gamma, probability=True)
        self.model.fit(X_train, y_train)
        
        # Calculate training accuracy
        train_accuracy = self.model.score(X_train, y_train)
        print(f"Training accuracy: {train_accuracy:.4f}")
        
        return train_accuracy
    
    def train_grid_search(self, X_train, y_train, strategy='ovr'):
        """
        Train SVM using grid search for hyperparameter optimization
        
        Parameters:
        -----------
        X_train : array-like
            Training data features
        y_train : array-like
            Training data labels
        strategy : str, default='ovr'
            Multiclass strategy: 'ovr' (One-vs-Rest), 'ovo' (One-vs-One), or 'standard'
        """
        # Define parameter grid
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'gamma': ['scale', 'auto', 0.01, 0.1, 1],
            'kernel': ['rbf', 'poly', 'linear']
        }
        
        # Select SVM strategy
        if strategy == 'ovr':
            print("\nTraining SVM with One-vs-Rest strategy and grid search...")
            # For OneVsRest, we need to prepend 'estimator__' to parameter names
            ovr_param_grid = {'estimator__' + k: v for k, v in param_grid.items()}
            base_estimator = SVC(probability=True)
            svm = OneVsRestClassifier(base_estimator)
            # Use correct parameter grid for OneVsRest
            param_grid = ovr_param_grid
        elif strategy == 'ovo':
            print("\nTraining SVM with One-vs-One strategy and grid search...")
            # For OneVsOne, we need to prepend 'estimator__' to parameter names
            ovo_param_grid = {'estimator__' + k: v for k, v in param_grid.items()}
            base_estimator = SVC(probability=True)
            svm = OneVsOneClassifier(base_estimator)
            # Use correct parameter grid for OneVsOne
            param_grid = ovo_param_grid
        else:  # standard
            print("\nTraining standard SVM with grid search...")
            svm = SVC(probability=True)
            # Standard SVC uses the original param_grid
        
        # Use grid search with cross-validation
        grid_search = GridSearchCV(svm, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        # Output best parameters
        print("\nBest SVM parameters:")
        print(grid_search.best_params_)
        print(f"Best cross-validation accuracy: {grid_search.best_score_:.4f}")
        
        # Save grid search results
        with open(os.path.join(self.output_dir, f'svm_grid_search_results_{strategy}.txt'), 'w') as f:
            f.write(f"Best parameters: {grid_search.best_params_}\n")
            f.write(f"Best validation accuracy: {grid_search.best_score_:.4f}\n\n")
            f.write("Top 5 parameter combinations:\n")
            
            # Sort results by mean test score and get top 5
            sorted_results = sorted(
                zip(grid_search.cv_results_['params'], grid_search.cv_results_['mean_test_score']),
                key=lambda x: x[1], reverse=True
            )
            
            for i, (params, score) in enumerate(sorted_results[:5]):
                f.write(f"{i+1}. {params}: {score:.4f}\n")
        
        # Set the best model
        self.model = grid_search.best_estimator_
        
        return grid_search.best_params_, grid_search.best_score_
    
    def train_ensemble(self, X_train, y_train, kernels=None, voting='hard'):
        """
        Train an ensemble of SVM models with different kernels
        
        Parameters:
        -----------
        X_train : array-like
            Training data features
        y_train : array-like
            Training data labels
        kernels : list of str, default=None
            List of kernels to use (default: ['linear', 'poly', 'rbf', 'sigmoid'])
        voting : str, default='hard'
            Voting strategy: 'hard' or 'soft'
        """
        from sklearn.ensemble import VotingClassifier
        
        if kernels is None:
            kernels = ['linear', 'poly', 'rbf', 'sigmoid']
            
        print(f"\nTraining SVM ensemble with kernels {kernels}...")
        
        # Create SVM classifiers with different kernels
        estimators = []
        for i, kernel in enumerate(kernels):
            svm = SVC(kernel=kernel, probability=(voting=='soft'))
            estimators.append((f'svm_{kernel}', svm))
        
        # Create and train voting classifier
        self.model = VotingClassifier(estimators=estimators, voting=voting)
        self.model.fit(X_train, y_train)
        
        # Calculate training accuracy
        train_accuracy = self.model.score(X_train, y_train)
        print(f"Training accuracy: {train_accuracy:.4f}")
        
        return train_accuracy
    
    def evaluate(self, X_test, y_test, class_names, filename_suffix=''):
        """
        Evaluate model on test data and generate reports
        
        Parameters:
        -----------
        X_test : array-like
            Test data features
        y_test : array-like
            Test data labels
        class_names : list of str
            Names of the classes
        filename_suffix : str, default=''
            Suffix to add to output filenames
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
        
        # If model supports probability predictions, generate ROC curves
        if hasattr(self.model, "predict_proba") or hasattr(self.model, "decision_function"):
            self.plot_roc_curves(X_test, y_test, class_names, filename_suffix)
        
        return test_accuracy, y_pred
    
    def plot_roc_curves(self, X_test, y_test, class_names, filename_suffix=''):
        """
        Plot ROC curves for multiclass classification
        
        Parameters:
        -----------
        X_test : array-like
            Test data features
        y_test : array-like
            Test data labels
        class_names : list of str
            Names of the classes
        filename_suffix : str, default=''
            Suffix to add to output filenames
        """
        from sklearn.metrics import roc_curve, auc
        from sklearn.preprocessing import label_binarize
        
        # Binarize the labels for multiclass ROC
        classes = np.unique(y_test)
        y_test_bin = label_binarize(y_test, classes=classes)
        n_classes = len(classes)
        
        # Get probabilities or decision function values
        if hasattr(self.model, "predict_proba"):
            y_score = self.model.predict_proba(X_test)
        else:  # Use decision function
            decision_values = self.model.decision_function(X_test)
            # Handle different output formats from decision_function
            if decision_values.ndim == 1:  # Binary classification
                y_score = np.column_stack([1-decision_values, decision_values])
            else:  # Already multiclass format
                y_score = decision_values
        
        # Compute ROC curve and ROC area for each class
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        
        for i in range(n_classes):
            # Some models might not return probabilities for all classes
            if i < y_score.shape[1]:
                fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
                roc_auc[i] = auc(fpr[i], tpr[i])
        
        # Plot ROC curves
        plt.figure(figsize=(12, 10))
        
        # Plot individual class ROC curves
        for i in range(n_classes):
            if i in roc_auc:  # Check if we have ROC data for this class
                plt.plot(fpr[i], tpr[i], lw=2,
                        label=f'{class_names[i]} (AUC = {roc_auc[i]:.2f})')
        
        # Plot random chance line
        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curves')
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, f'roc_curves{filename_suffix}.png'))
        plt.close()
    
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
        """Get probability estimates for each class"""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        else:
            raise ValueError("This model does not support probability estimates") 