# Standard library imports
import os
import sys
import argparse
import time

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Third-party imports - data analysis and scientific computing
import numpy as np
import pandas as pd

# Third-party imports - machine learning
from sklearn.metrics import accuracy_score

# Third-party imports - visualization
import matplotlib.pyplot as plt

# Import custom modules - dataset operations
from dataset.load import load_data, load_image_data, standardize_features
from dataset.load import extract_basic_features, extract_advanced_features
from dataset.augmentation import augment_rock_dataset
from dataset.check import check_dataset

# Import custom modules - classifiers
from classifier.knn import KNNClassifier
from classifier.svm import SVMClassifier
from classifier.cnn import CNNClassifier

# Import custom modules - dimensionality reduction
from dim_reducer.lda import LDADimensionReducer
from dim_reducer.pca import PCA

class HierarchicalRockClassifier:
    """Hierarchical rock classifier that first sub-divides each rock type into clusters"""
    
    def __init__(self, output_dir='./output'):
        """
        Initialize hierarchical rock classifier
        
        Parameters:
        -----------
        output_dir : str
            Output directory for results
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Store rock type classifiers and subclass models
        self.rock_type_classifier = None
        self.subclass_classifiers = {}
        self.rock_types = None
        self.num_subclasses_per_type = {}
        self.subclass_to_rock_mapping = {}
        
        # 存储降维模型，用于在预测时应用
        self.dim_reduction_method = None  # 'pca', 'lda', or None
        self.dim_reducer = None  # 保存降维模型
        
    def train(self, X_train, y_train, X_valid, y_valid, rock_types, 
              classifier_type='knn', num_subclasses=3, dim_reduction=None,
              pca_components=None, lda_components=None, advanced_features=False):
        """
        Train the hierarchical classifier
        
        Parameters:
        -----------
        X_train : array-like
            Training features
        y_train : array-like
            Training labels
        X_valid : array-like
            Validation features
        y_valid : array-like
            Validation labels
        rock_types : list
            List of rock type names
        classifier_type : str
            Type of classifier to use ('knn', 'svm', or 'cnn')
        num_subclasses : int
            Number of subclasses per rock type
        dim_reduction : str or None
            Dimensionality reduction method ('pca', 'lda', or None)
        pca_components : int or None
            Number of PCA components
        lda_components : int or None
            Number of LDA components
        advanced_features : bool
            Whether to use advanced feature extraction
            
        Returns:
        --------
        self : HierarchicalRockClassifier
            Trained classifier
        """
        self.rock_types = rock_types
        print(f"\nTraining hierarchical classifier with {classifier_type} and {num_subclasses} subclasses per rock type")
        print(f"Dimensionality reduction: {dim_reduction if dim_reduction else 'None'}")
        
        # 保存降维方法，用于预测时应用
        self.dim_reduction_method = dim_reduction
        
        # Step 1: Apply dimensionality reduction if requested
        if dim_reduction == 'pca':
            X_train_reduced, X_valid_reduced, self.dim_reducer = self._apply_pca(X_train, X_valid, pca_components)
        elif dim_reduction == 'lda':
            X_train_reduced, X_valid_reduced, self.dim_reducer = self._apply_lda(X_train, y_train, X_valid, lda_components)
        else:
            X_train_reduced, X_valid_reduced = X_train, X_valid
        
        # Step 2: Divide each rock type into subclasses using clustering
        self._create_subclasses(X_train_reduced, y_train, num_subclasses)
        
        # Step 3: Train subclass classifiers for each rock type
        self._train_subclass_classifiers(X_train_reduced, y_train, X_valid_reduced, y_valid, 
                                         classifier_type, advanced_features)
        
        # Step 4: Train rock type classifier
        self._train_rock_type_classifier(X_train_reduced, y_train, X_valid_reduced, y_valid, 
                                        classifier_type, advanced_features)
        
        return self
    
    def _create_subclasses(self, X, y, num_subclasses):
        """
        Create subclasses for each rock type using K-means clustering
        
        Parameters:
        -----------
        X : array-like
            Features
        y : array-like
            Rock type labels
        num_subclasses : int
            Number of subclasses per rock type
        """
        from sklearn.cluster import KMeans
        
        print("\nCreating subclasses for each rock type using clustering:")
        
        # For each rock type, cluster the samples
        for rock_idx, rock_type in enumerate(self.rock_types):
            # Get samples for this rock type
            mask = (y == rock_idx)
            X_rock = X[mask]
            
            # Skip if too few samples
            if len(X_rock) < num_subclasses:
                print(f"  {rock_type}: not enough samples ({len(X_rock)}), using 1 subclass")
                self.num_subclasses_per_type[rock_idx] = 1
                continue
            
            # Apply K-means clustering
            kmeans = KMeans(n_clusters=num_subclasses, random_state=42, n_init=10)
            subclass_labels = kmeans.fit_predict(X_rock)
            
            # Store the K-means model
            self.subclass_classifiers[f"cluster_{rock_idx}"] = kmeans
            self.num_subclasses_per_type[rock_idx] = num_subclasses
            
            # Count samples per subclass
            for subclass_idx in range(num_subclasses):
                subclass_count = np.sum(subclass_labels == subclass_idx)
                print(f"  {rock_type} - Subclass {subclass_idx}: {subclass_count} samples")
                
                # Create mapping from subclass to rock type
                global_subclass_idx = rock_idx * num_subclasses + subclass_idx
                self.subclass_to_rock_mapping[global_subclass_idx] = rock_idx
        
        print(f"Total subclasses: {sum(self.num_subclasses_per_type.values())}")
    
    def _apply_pca(self, X_train, X_valid, n_components=None):
        """Apply PCA dimensionality reduction"""
        # 设置matplotlib使用非交互式后端
        import matplotlib
        matplotlib.use('Agg')
        
        pca_dir = os.path.join(self.output_dir, 'pca')
        os.makedirs(pca_dir, exist_ok=True)
        
        print("\nApplying PCA for dimensionality reduction...")
        pca = PCA(n_components=n_components, output_dir=pca_dir)
        
        # Fit and transform data
        X_train_pca = pca.fit_transform(X_train)
        X_valid_pca = pca.transform(X_valid)
        
        # Determine number of components to use (if not specified)
        if n_components is None:
            # Find number of components that explain 95% of variance
            cumulative_var = np.cumsum(pca.explained_variance_ratio)
            n_components = np.argmax(cumulative_var >= 0.95) + 1
            print(f"Using {n_components} PCA components (explains 95% of variance)")
            
            # Update data to use only these components
            X_train_pca = X_train_pca[:, :n_components]
            X_valid_pca = X_valid_pca[:, :n_components]
        
        # Visualize PCA results
        pca.plot_explained_variance(max_components=min(50, len(pca.explained_variance)))
        
        return X_train_pca, X_valid_pca, pca
    
    def _apply_lda(self, X_train, y_train, X_valid, n_components=None):
        """Apply LDA dimensionality reduction"""
        # 设置matplotlib使用非交互式后端
        import matplotlib
        matplotlib.use('Agg')
        
        lda_dir = os.path.join(self.output_dir, 'lda')
        os.makedirs(lda_dir, exist_ok=True)
        
        print("\nApplying LDA for dimensionality reduction...")
        # For LDA, number of components is limited by number of classes
        max_lda_components = min(len(np.unique(y_train)) - 1, X_train.shape[1])
        
        if n_components is None:
            n_components = max_lda_components
        else:
            n_components = min(n_components, max_lda_components)
        
        print(f"Using {n_components} LDA components")
        
        # Create and fit LDA model
        lda = LDADimensionReducer(output_dir=lda_dir)
        X_train_lda = lda.fit_transform(X_train, y_train, n_components)
        X_valid_lda = lda.transform(X_valid)
        
        return X_train_lda, X_valid_lda, lda
    
    def _train_subclass_classifiers(self, X_train, y_train, X_valid, y_valid, classifier_type, advanced_features=False):
        """Train classifiers for each rock type to determine subclass"""
        print("\nTraining subclass classifiers for each rock type:")
        
        # For each rock type, train a classifier to identify the subclass
        for rock_idx, rock_type in enumerate(self.rock_types):
            # Skip if only one subclass
            if self.num_subclasses_per_type.get(rock_idx, 0) <= 1:
                continue
                
            # Get samples for this rock type
            mask_train = (y_train == rock_idx)
            X_train_rock = X_train[mask_train]
            
            mask_valid = (y_valid == rock_idx)
            X_valid_rock = X_valid[mask_valid]
            
            # Get subclass labels for this rock type using existing KMeans model
            # 注意：KMeans模型现在是在降维后的特征空间上训练的，因此预测时应该使用相同的特征空间
            kmeans = self.subclass_classifiers[f"cluster_{rock_idx}"]
            y_train_subclass = kmeans.predict(X_train_rock)
            
            if len(X_valid_rock) > 0:
                y_valid_subclass = kmeans.predict(X_valid_rock)
            else:
                y_valid_subclass = np.array([])
            
            # Create appropriate classifier
            subclass_output_dir = os.path.join(self.output_dir, f"subclass_{rock_type}")
            os.makedirs(subclass_output_dir, exist_ok=True)
            
            if classifier_type == 'knn':
                classifier = KNNClassifier(output_dir=subclass_output_dir)
                
                if advanced_features:
                    print(f"  {rock_type}: Training KNN with grid search")
                    classifier.train_grid_search(X_train_rock, y_train_subclass)
                else:
                    print(f"  {rock_type}: Training standard KNN")
                    classifier.train_standard(X_train_rock, y_train_subclass,
                                          X_valid_rock, y_valid_subclass if len(X_valid_rock) > 0 else None)
                                          
            elif classifier_type == 'svm':
                classifier = SVMClassifier(output_dir=subclass_output_dir)
                print(f"  {rock_type}: Training SVM with grid search")
                classifier.train_grid_search(X_train_rock, y_train_subclass)
                
            else:  # CNN not applicable for subclass classification in this implementation
                raise ValueError("CNN classifier not supported for subclass classification")
            
            # Save classifier
            self.subclass_classifiers[f"classifier_{rock_idx}"] = classifier
            
            # Evaluate on validation set
            if len(X_valid_rock) > 0:
                accuracy = accuracy_score(y_valid_subclass, classifier.predict(X_valid_rock))
                print(f"  {rock_type} subclass validation accuracy: {accuracy:.4f}")
    
    def _train_rock_type_classifier(self, X_train, y_train, X_valid, y_valid, classifier_type, advanced_features=False):
        """Train classifier to identify rock type"""
        print("\nTraining main rock type classifier:")
        
        rock_type_output_dir = os.path.join(self.output_dir, "rock_type_classifier")
        os.makedirs(rock_type_output_dir, exist_ok=True)
        
        if classifier_type == 'knn':
            classifier = KNNClassifier(output_dir=rock_type_output_dir)
            
            if advanced_features:
                print("  Training KNN with grid search")
                classifier.train_grid_search(X_train, y_train)
            else:
                print("  Training standard KNN")
                classifier.train_standard(X_train, y_train, X_valid, y_valid)
                
        elif classifier_type == 'svm':
            classifier = SVMClassifier(output_dir=rock_type_output_dir)
            print("  Training SVM with grid search")
            classifier.train_grid_search(X_train, y_train)
            
        elif classifier_type == 'cnn':
            classifier = CNNClassifier(output_dir=rock_type_output_dir)
            print("  Training CNN")
            # Assuming X_train and X_valid are image paths for CNN
            classifier.train(X_train, y_train, X_valid, y_valid, 
                          class_names=self.rock_types, epochs=10)
        
        # Save classifier
        self.rock_type_classifier = classifier
        
        # Evaluate on validation set
        if len(X_valid) > 0:
            accuracy = accuracy_score(y_valid, classifier.predict(X_valid))
            print(f"  Rock type validation accuracy: {accuracy:.4f}")
    
    def predict(self, X):
        """
        Predict rock type with hierarchical classification
        
        Parameters:
        -----------
        X : array-like
            Features to predict
            
        Returns:
        --------
        y_pred : array-like
            Predicted rock type labels
        subclass_preds : array-like
            Predicted subclass labels
        """
        if self.rock_type_classifier is None:
            raise ValueError("Classifier has not been trained yet")
            
        # 首先应用与训练时相同的降维
        if self.dim_reduction_method == 'pca' and self.dim_reducer is not None:
            X_reduced = self.dim_reducer.transform(X)
        elif self.dim_reduction_method == 'lda' and self.dim_reducer is not None:
            X_reduced = self.dim_reducer.transform(X)
        else:
            X_reduced = X
            
        # Step 1: Predict rock type
        rock_type_preds = self.rock_type_classifier.predict(X_reduced)
        
        # Step 2: For each sample, predict subclass based on predicted rock type
        subclass_preds = np.zeros_like(rock_type_preds)
        
        for i, rock_idx in enumerate(rock_type_preds):
            # If no subclasses for this rock type, skip
            if self.num_subclasses_per_type.get(rock_idx, 0) <= 1:
                subclass_preds[i] = rock_idx  # Use rock type as subclass
                continue
                
            # Get sample
            X_sample = X_reduced[i:i+1]
            
            # If we have a subclass classifier for this rock type, use it
            if f"classifier_{rock_idx}" in self.subclass_classifiers:
                classifier = self.subclass_classifiers[f"classifier_{rock_idx}"]
                # 这里使用的X_sample已经是降维后的特征，所以不需要做额外处理
                local_subclass = classifier.predict(X_sample)[0]
                
                # Convert local subclass to global subclass index
                subclass_preds[i] = rock_idx * max(self.num_subclasses_per_type.values()) + local_subclass
            else:
                # Use clustering directly
                kmeans = self.subclass_classifiers.get(f"cluster_{rock_idx}")
                if kmeans is not None:
                    # KMeans已经在降维后的特征空间上训练，所以使用降维后的特征预测
                    local_subclass = kmeans.predict(X_sample)[0]
                    subclass_preds[i] = rock_idx * max(self.num_subclasses_per_type.values()) + local_subclass
                else:
                    subclass_preds[i] = rock_idx  # Fall back to rock type
        
        return rock_type_preds, subclass_preds
    
    def evaluate(self, X_test, y_test, detailed=True):
        """
        Evaluate the hierarchical classifier
        
        Parameters:
        -----------
        X_test : array-like
            Test features
        y_test : array-like
            Test labels
        detailed : bool
            Whether to print detailed evaluation
            
        Returns:
        --------
        metrics : dict
            Evaluation metrics
        """
        # 设置matplotlib使用非交互式后端
        import matplotlib
        matplotlib.use('Agg')
        
        # 首先应用与训练时相同的降维
        if self.dim_reduction_method == 'pca' and self.dim_reducer is not None:
            print("\nApplying PCA dimensionality reduction to test data...")
            X_test_reduced = self.dim_reducer.transform(X_test)
        elif self.dim_reduction_method == 'lda' and self.dim_reducer is not None:
            print("\nApplying LDA dimensionality reduction to test data...")
            X_test_reduced = self.dim_reducer.transform(X_test)
        else:
            X_test_reduced = X_test
        
        # 使用降维后的特征进行预测
        rock_type_preds, subclass_preds = self.predict(X_test_reduced)
        
        # Calculate rock type accuracy
        rock_type_accuracy = accuracy_score(y_test, rock_type_preds)
        
        # Create a mapping from subclass predictions to rock types
        # (useful for validation when comparing to ground truth rock types)
        predicted_rock_types_from_subclass = np.array([
            self.subclass_to_rock_mapping.get(subclass, subclass) 
            for subclass in subclass_preds
        ])
        
        subclass_to_rock_accuracy = accuracy_score(y_test, predicted_rock_types_from_subclass)
        
        # Print results
        print("\nEvaluation results:")
        print(f"  Rock type accuracy: {rock_type_accuracy:.4f}")
        print(f"  Subclass-derived rock type accuracy: {subclass_to_rock_accuracy:.4f}")
        
        # Create confusion matrix for rock types
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_test, rock_type_preds)
        
        # Plot confusion matrix
        plt.figure(figsize=(10, 8))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion Matrix')
        plt.colorbar()
        tick_marks = np.arange(len(self.rock_types))
        plt.xticks(tick_marks, self.rock_types, rotation=45, ha='right')
        plt.yticks(tick_marks, self.rock_types)
        
        # Add text annotations
        thresh = cm.max() / 2
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, format(cm[i, j], 'd'),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.savefig(os.path.join(self.output_dir, 'confusion_matrix.png'))
        plt.close('all')
        
        # If detailed evaluation is requested
        if detailed:
            # Evaluate per rock type accuracy
            for rock_idx, rock_type in enumerate(self.rock_types):
                mask = (y_test == rock_idx)
                if np.sum(mask) == 0:
                    continue
                    
                rock_accuracy = accuracy_score(y_test[mask], rock_type_preds[mask])
                print(f"  {rock_type} accuracy: {rock_accuracy:.4f}")
            
            # For each rock type, evaluate subclass accuracy if applicable
            for rock_idx, rock_type in enumerate(self.rock_types):
                # Skip if only one subclass or no classifier
                if self.num_subclasses_per_type.get(rock_idx, 0) <= 1 or \
                   f"classifier_{rock_idx}" not in self.subclass_classifiers:
                    continue
                
                # Get samples for this rock type
                mask = (y_test == rock_idx)
                X_test_rock = X_test_reduced[mask]  # 使用降维后的特征
                
                # Skip if no samples
                if len(X_test_rock) == 0:
                    continue
                
                # Get subclass predictions using the clustering model
                kmeans = self.subclass_classifiers[f"cluster_{rock_idx}"]
                
                # KMeans模型在降维后的特征空间上训练
                true_subclasses = kmeans.predict(X_test_rock)
                
                # Use the classifier to predict subclasses
                classifier = self.subclass_classifiers[f"classifier_{rock_idx}"]
                pred_subclasses = classifier.predict(X_test_rock)
                
                # Calculate subclass accuracy
                subclass_accuracy = accuracy_score(true_subclasses, pred_subclasses)
                print(f"  {rock_type} subclass accuracy: {subclass_accuracy:.4f}")
        
        # Return evaluation metrics
        return {
            'rock_type_accuracy': rock_type_accuracy,
            'subclass_to_rock_accuracy': subclass_to_rock_accuracy,
            'rock_type_predictions': rock_type_preds,
            'subclass_predictions': subclass_preds
        }
    
    def save(self, filename='hierarchical_model'):
        """Save the hierarchical classifier"""
        import joblib
        
        # Create a dictionary with all necessary objects
        model_dict = {
            'rock_type_classifier': self.rock_type_classifier,
            'subclass_classifiers': self.subclass_classifiers,
            'rock_types': self.rock_types,
            'num_subclasses_per_type': self.num_subclasses_per_type,
            'subclass_to_rock_mapping': self.subclass_to_rock_mapping,
            'dim_reduction_method': self.dim_reduction_method,
            'dim_reducer': self.dim_reducer
        }
        
        # Save the dictionary
        model_path = os.path.join(self.output_dir, f"{filename}.pkl")
        joblib.dump(model_dict, model_path)
        
        print(f"\nModel saved to {model_path}")
        return model_path
    
    def load(self, model_path):
        """Load a saved hierarchical classifier"""
        import joblib
        
        # Load the model dictionary
        model_dict = joblib.load(model_path)
        
        # Restore all objects
        self.rock_type_classifier = model_dict['rock_type_classifier']
        self.subclass_classifiers = model_dict['subclass_classifiers']
        self.rock_types = model_dict['rock_types']
        self.num_subclasses_per_type = model_dict['num_subclasses_per_type']
        self.subclass_to_rock_mapping = model_dict['subclass_to_rock_mapping']
        
        # 恢复降维相关的属性
        self.dim_reduction_method = model_dict.get('dim_reduction_method', None)
        self.dim_reducer = model_dict.get('dim_reducer', None)
        
        print(f"Model loaded from {model_path}")
        return self

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Hierarchical Rock Image Classification')
    
    # Dataset arguments
    parser.add_argument('--data-dir', type=str, default='./data/RockData',
                       help='Path to the dataset directory')
    parser.add_argument('--augment', action='store_true',
                       help='Whether to augment the dataset')
    parser.add_argument('--augmentations-per-image', type=int, default=5,
                       help='Number of augmentations per image')
    
    # Feature extraction arguments
    parser.add_argument('--advanced-features', action='store_true',
                       help='Use advanced feature extraction (texture, color, shape)')
    
    # Classifier selection
    parser.add_argument('--classifier', type=str, choices=['knn', 'svm', 'cnn'], default='knn',
                       help='Classifier to use (knn, svm, or cnn)')
    
    # Hierarchical parameters
    parser.add_argument('--subclasses', type=int, default=3,
                       help='Number of subclasses per rock type')
    
    # Dimensionality reduction arguments
    parser.add_argument('--dim-reduction', type=str, choices=['none', 'pca', 'lda'], default='none',
                       help='Dimensionality reduction method to use')
    parser.add_argument('--pca-components', type=int, default=None,
                       help='Number of PCA components to use (default: auto-determined)')
    parser.add_argument('--lda-components', type=int, default=None,
                       help='Number of LDA components to use (default: auto-determined)')
    
    # Output arguments
    parser.add_argument('--output-dir', type=str, default='./output',
                       help='Output directory for results')
    
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_args()
    
    # Create timestamp for output directory
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(args.output_dir, f"hierarchical_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare dataset
    data_dir = args.data_dir
    
    # Check if data directory exists, if not create example structure
    if not os.path.exists(data_dir):
        print(f"\nData directory '{data_dir}' not found. Creating example directory structure...")
        os.makedirs(data_dir, exist_ok=True)
        
        # Create train, valid, test directories
        for split in ['train', 'valid', 'test']:
            split_dir = os.path.join(data_dir, split)
            os.makedirs(split_dir, exist_ok=True)
            
            # Create example rock class directories
            for rock_class in ['igneous', 'sedimentary', 'metamorphic']:
                os.makedirs(os.path.join(split_dir, rock_class), exist_ok=True)
        
        print(f"Created example directory structure in '{data_dir}'")
        print("Please add rock images to each class folder before running the classifier.")
        print("Example structure:")
        print(f"  {data_dir}/")
        print(f"  ├── train/")
        print(f"  │   ├── igneous/")
        print(f"  │   ├── sedimentary/")
        print(f"  │   └── metamorphic/")
        print(f"  ├── valid/")
        print(f"  │   ├── igneous/")
        print(f"  │   ├── sedimentary/")
        print(f"  │   └── metamorphic/")
        print(f"  └── test/")
        print(f"      ├── igneous/")
        print(f"      ├── sedimentary/")
        print(f"      └── metamorphic/")
        return
    
    # Augment dataset if requested
    if args.augment:
        # Get the parent directory of data_dir
        data_parent = os.path.dirname(os.path.abspath(data_dir))
        augmented_dir = os.path.join(data_parent, f"Augmented_{os.path.basename(data_dir)}")
        
        print(f"\nAugmenting dataset from {data_dir} to {augmented_dir}")
        augmented_dir = augment_rock_dataset(data_dir, augmented_dir, args.augmentations_per_image)
        
        # Use the augmented dataset for further processing
        data_dir = augmented_dir
        print(f"Using augmented dataset at: {data_dir}")
    
    # Check dataset
    stats = check_dataset(data_dir)
    
    # Check if we have any images
    if stats.get('total_images', 0) == 0:
        print("\nNo images found in the dataset. Please add images to the dataset and try again.")
        return
    
    # Get rock classes
    train_dir = os.path.join(data_dir, 'train')
    valid_dir = os.path.join(data_dir, 'valid')
    test_dir = os.path.join(data_dir, 'test')
    
    rock_classes = sorted([d for d in os.listdir(train_dir) 
                         if os.path.isdir(os.path.join(train_dir, d))])
    print(f"Rock types: {rock_classes}")
    print(f"Total classes: {len(rock_classes)}")
    
    # Select feature extractor
    if args.advanced_features:
        feature_extractor = extract_advanced_features
        print("Using advanced feature extraction")
    else:
        feature_extractor = extract_basic_features
        print("Using basic feature extraction")
    
    # For CNN, load image paths
    if args.classifier == 'cnn':
        X_train, y_train = load_image_data(train_dir, rock_classes)
        X_valid, y_valid = load_image_data(valid_dir, rock_classes)
        X_test, y_test = load_image_data(test_dir, rock_classes)
        
        print(f"Training set: {len(X_train)} samples")
        print(f"Validation set: {len(X_valid)} samples")
        print(f"Test set: {len(X_test)} samples")
    else:
        # Load and extract features
        print("\nLoading and extracting features...")
        X_train, y_train = load_data(train_dir, rock_classes, feature_extractor)
        X_valid, y_valid = load_data(valid_dir, rock_classes, feature_extractor)
        X_test, y_test = load_data(test_dir, rock_classes, feature_extractor)
        
        print(f"Training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
        print(f"Validation set: {X_valid.shape[0]} samples")
        print(f"Test set: {X_test.shape[0]} samples")
        
        # Standardize features (not applicable for CNN)
        print("\nStandardizing features...")
        (X_train_scaled, X_valid_scaled, X_test_scaled), scaler = standardize_features(
            X_train, X_valid, X_test)
        
        # Update variables to use scaled features
        X_train, X_valid, X_test = X_train_scaled, X_valid_scaled, X_test_scaled
    
    # Create and train hierarchical classifier
    dim_reduction = None if args.dim_reduction == 'none' else args.dim_reduction
    
    hierarchical_classifier = HierarchicalRockClassifier(output_dir=output_dir)
    hierarchical_classifier.train(
        X_train, y_train, X_valid, y_valid, rock_classes,
        classifier_type=args.classifier,
        num_subclasses=args.subclasses,
        dim_reduction=dim_reduction,
        pca_components=args.pca_components,
        lda_components=args.lda_components,
        advanced_features=args.advanced_features
    )
    
    # Evaluate on test set
    hierarchical_classifier.evaluate(X_test, y_test)
    
    # Save the model
    hierarchical_classifier.save()
    
    print("\nTraining and evaluation complete.")

if __name__ == '__main__':
    main()
