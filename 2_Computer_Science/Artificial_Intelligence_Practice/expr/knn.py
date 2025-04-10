import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib

class KNNClassifier:
    """K-Nearest Neighbors classifier implementation with training and evaluation methods"""
    
    def __init__(self, output_dir='./output'):
        """Initialize KNN classifier"""
        self.model = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def train_basic(self, X_train, y_train, X_valid, y_valid, k_values=None):
        """Train KNN using a list of K values and basic validation"""
        if k_values is None:
            k_values = [1, 3, 5, 7, 9, 11, 13, 15]
            
        best_accuracy = 0
        best_k = 0
        accuracy_list = []
        
        print("\nTraining KNN model with different K values...")
        
        for k in k_values:
            # Create and train KNN classifier
            knn = KNeighborsClassifier(n_neighbors=k, weights='distance', n_jobs=-1)
            knn.fit(X_train, y_train)
            
            # Evaluate on validation set
            y_pred = knn.predict(X_valid)
            accuracy = accuracy_score(y_valid, y_pred)
            accuracy_list.append(accuracy)
            
            print(f"K = {k}: Validation accuracy = {accuracy:.4f}")
            
            # Save best model
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_k = k
                self.model = knn
        
        print(f"\nBest K value = {best_k}, Validation accuracy = {best_accuracy:.4f}")
        
        # Visualize effect of different K values
        plt.figure(figsize=(10, 6))
        plt.plot(k_values, accuracy_list, 'o-')
        plt.xlabel('K value')
        plt.ylabel('Validation accuracy')
        plt.title('KNN Classification Accuracy with Different K Values')
        plt.grid(True)
        plt.savefig(os.path.join(self.output_dir, 'knn_k_values.png'))
        plt.close()
        
        return best_k, best_accuracy
    
    def train_advanced(self, X_train, y_train):
        """Train KNN using grid search for hyperparameter optimization"""
        param_grid = {
            'n_neighbors': [3, 5, 7, 9, 11, 13],
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan', 'minkowski']
        }
        
        print("\nUsing grid search to find optimal KNN parameters...")
        knn = KNeighborsClassifier()
        grid_search = GridSearchCV(knn, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        # Output best parameters
        print("\nBest KNN parameters:")
        print(grid_search.best_params_)
        print(f"Best cross-validation accuracy: {grid_search.best_score_:.4f}")
        
        # Save grid search results
        with open(os.path.join(self.output_dir, 'grid_search_results.txt'), 'w') as f:
            f.write(f"Best parameters: {grid_search.best_params_}\n")
            f.write(f"Best validation accuracy: {grid_search.best_score_:.4f}\n\n")
            f.write("All results:\n")
            for i, params in enumerate(grid_search.cv_results_['params']):
                f.write(f"{params}: {grid_search.cv_results_['mean_test_score'][i]:.4f}\n")
        
        # Set the best model
        self.model = grid_search.best_estimator_
        
        return grid_search.best_params_, grid_search.best_score_
    
    def evaluate(self, X_test, y_test, class_names, filename_suffix=''):
        """Evaluate model on test data and generate reports"""
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
        
        return test_accuracy, y_pred
    
    def save_model(self, filename='knn_model.pkl'):
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