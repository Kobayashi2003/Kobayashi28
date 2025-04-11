import os
import argparse
import numpy as np
from sklearn.metrics import classification_report, accuracy_score
from sklearn.cluster import KMeans

# Import local modules
from utils.load_dataset import load_dataset
from utils.check_dataset import check_dataset
from utils.augmentate_dataset import augment_dataset, augment_class_balanced
from dim_reducer.pca import PCAdimReducer
from dim_reducer.lda import LDAdimReducer
from classifier.knn import KNNClassifier
from classifier.svm import SVMClassifier
from classifier.cnn import CNNClassifier
from classifier.dbscan import DBSCANClassifier

def parse_args():
    parser = argparse.ArgumentParser(description="Train a classifier on image data")
    
    # Dataset options
    parser.add_argument("--data_dir", type=str, default="../data", 
                        help="Path to dataset directory")
    parser.add_argument("--img_size", nargs=2, type=int, default=[224, 224], 
                        help="Image size (width, height)")
    parser.add_argument("--grayscale", action="store_true", 
                        help="Convert images to grayscale")
    
    # Data augmentation options
    parser.add_argument("--augment", action="store_true", 
                        help="Use data augmentation")
    parser.add_argument("--augment_factor", type=int, default=2,
                        help="Number of augmented samples to create per original sample")
    parser.add_argument("--balance_classes", action="store_true",
                        help="Balance classes using augmentation")
    
    # Dimension reduction options
    parser.add_argument("--dim_reducer", type=str, choices=["none", "pca", "lda"], default="none",
                        help="Dimension reduction method")
    parser.add_argument("--pca_components", type=float, default=0.95,
                        help="Number of components or variance ratio for PCA (0-1 for variance ratio, >1 for num components)")
    parser.add_argument("--lda_components", type=int, default=None,
                        help="Number of components for LDA (max: n_classes-1)")
    parser.add_argument("--pca_before_lda", action="store_true",
                        help="Apply PCA before LDA (recommended for high-dimensional data)")
    parser.add_argument("--pca_for_lda_components", type=int, default=None,
                        help="Number of PCA components to use before LDA (default: min(n_features, max(500, n_classes*10)))")
    
    # Classification options
    parser.add_argument("--classifier", type=str, choices=["knn", "svm", "cnn", "dbscan"], default="knn",
                        help="Classifier type")
    parser.add_argument("--n_neighbors", type=int, default=5,
                        help="Number of neighbors for KNN classifier")
    parser.add_argument("--kernel", type=str, default="rbf",
                        help="Kernel type for SVM classifier")
    
    # Sub-classification options
    parser.add_argument("--use_subclasses", action="store_true",
                        help="Use unsupervised subclassification before classification")
    parser.add_argument("--min_subclasses", type=int, default=2,
                        help="Minimum number of subclasses per original class")
    parser.add_argument("--max_subclasses", type=int, default=5,
                        help="Maximum number of subclasses per original class")
    parser.add_argument("--min_samples_per_subclass", type=int, default=5,
                        help="Minimum samples required for a valid subclass")
    
    return parser.parse_args()

def create_subclasses(X, y, min_subclasses, max_subclasses, min_samples_per_subclass):
    """
    Create subclasses for each original class using K-means clustering
    
    Args:
        X: Features, shape (n_samples, n_features)
        y: Original class labels
        min_subclasses: Minimum number of subclasses per original class
        max_subclasses: Maximum number of subclasses per original class
        min_samples_per_subclass: Minimum samples required per subclass
        
    Returns:
        X_sub: Original features
        y_sub: New subclass labels
        subclass_to_original: Mapping from subclass to original class
    """
    unique_classes = np.unique(y)
    next_subclass_id = 0
    
    # Initialize empty arrays for new dataset
    X_with_subclasses = []
    y_with_subclasses = []
    subclass_to_original = {}
    
    print("Creating subclasses for each original class:")
    
    for original_class in unique_classes:
        # Get samples for this class
        class_mask = (y == original_class)
        X_class = X[class_mask]
        num_samples = X_class.shape[0]
        
        # Determine number of clusters for this class
        # More samples -> more clusters, up to max_subclasses
        max_possible_clusters = min(max_subclasses, num_samples // min_samples_per_subclass)
        if max_possible_clusters < min_subclasses:
            # If too few samples for multiple clusters, use just one
            num_clusters = 1
        else:
            num_clusters = np.random.randint(min_subclasses, max_possible_clusters + 1)
        
        print(f"  Class {original_class}: {num_samples} samples -> {num_clusters} subclasses")
        
        if num_clusters == 1:
            # Just one cluster, assign all to the same subclass
            X_with_subclasses.append(X_class)
            y_with_subclasses.append(np.full(X_class.shape[0], next_subclass_id))
            subclass_to_original[next_subclass_id] = original_class
            next_subclass_id += 1
        else:
            # Use K-means for clustering
            # Reshape if needed
            if len(X_class.shape) > 2:
                X_class_reshaped = X_class.reshape(X_class.shape[0], -1)
            else:
                X_class_reshaped = X_class
                
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(X_class_reshaped)
            
            # Check each subclass for minimum samples
            for cluster_id in range(num_clusters):
                cluster_mask = (cluster_labels == cluster_id)
                cluster_size = np.sum(cluster_mask)
                
                if cluster_size >= min_samples_per_subclass:
                    # Add this subclass to the new dataset
                    X_with_subclasses.append(X_class[cluster_mask])
                    y_with_subclasses.append(np.full(cluster_size, next_subclass_id))
                    subclass_to_original[next_subclass_id] = original_class
                    next_subclass_id += 1
                    print(f"    Subclass {next_subclass_id-1}: {cluster_size} samples")
                else:
                    print(f"    Skipping small subclass with only {cluster_size} samples")
    
    # Combine all subclasses into a single dataset
    X_sub = np.vstack(X_with_subclasses)
    y_sub = np.concatenate(y_with_subclasses)
    
    print(f"Created {next_subclass_id} subclasses from {len(unique_classes)} original classes")
    
    return X_sub, y_sub, subclass_to_original

def map_predictions_to_original(y_pred, subclass_to_original):
    """
    Map subclass predictions back to original classes
    
    Args:
        y_pred: Predictions with subclass labels
        subclass_to_original: Mapping from subclass to original class
        
    Returns:
        Original class predictions
    """
    return np.array([subclass_to_original[subclass] for subclass in y_pred])

def main():
    args = parse_args()
    
    # Check dataset structure
    print("Checking dataset structure...")
    check_dataset(args.data_dir)
    
    # Load dataset
    print("Loading dataset...")
    data = load_dataset(args.data_dir, img_size=tuple(args.img_size), convert_to_grayscale=args.grayscale)
    X_train, y_train = data['X_train'], data['y_train']
    X_valid, y_valid = data['X_valid'], data['y_valid']
    X_test, y_test = data['X_test'], data['y_test']
    class_names = data['class_names']
    
    print(f"Loaded dataset with {len(X_train)} training, {len(X_valid)} validation, and {len(X_test)} test samples")
    print(f"Classes: {class_names}")
    
    # Data preprocessing 
    # Normalize pixel values to [0, 1]
    X_train = X_train.astype(np.float32) / 255.0
    X_valid = X_valid.astype(np.float32) / 255.0
    X_test = X_test.astype(np.float32) / 255.0
    
    # Apply data augmentation if specified
    if args.augment:
        print(f"Applying data augmentation with factor {args.augment_factor}...")
        X_train_aug, y_train_aug = augment_dataset(X_train, y_train, num_augmentations=args.augment_factor)
        print(f"Augmented training data: {X_train.shape} → {X_train_aug.shape}")
        
        # Update training data with augmented data
        X_train, y_train = X_train_aug, y_train_aug
    
    # Balance classes if specified
    if args.balance_classes:
        print("Balancing classes using augmentation...")
        # Get class distribution before balancing
        unique_classes, class_counts = np.unique(y_train, return_counts=True)
        for class_idx, count in zip(unique_classes, class_counts):
            print(f"  Class {class_names[class_idx]}: {count} samples")
        
        # Apply class balancing
        X_train_balanced, y_train_balanced = augment_class_balanced(X_train, y_train)
        
        # Get class distribution after balancing
        unique_classes, class_counts = np.unique(y_train_balanced, return_counts=True)
        print("Class distribution after balancing:")
        for class_idx, count in zip(unique_classes, class_counts):
            print(f"  Class {class_names[class_idx]}: {count} samples")
        
        # Update training data with balanced data
        X_train, y_train = X_train_balanced, y_train_balanced
    
    # Perform dimension reduction if specified
    if args.dim_reducer != "none":
        print(f"Performing {args.dim_reducer.upper()} dimension reduction...")
        
        # Reshape data to 2D if needed for dimension reduction
        if len(X_train.shape) > 2:
            n_samples_train = X_train.shape[0]
            n_samples_valid = X_valid.shape[0]
            n_samples_test = X_test.shape[0]
            
            X_train_reshaped = X_train.reshape(n_samples_train, -1)
            X_valid_reshaped = X_valid.reshape(n_samples_valid, -1)
            X_test_reshaped = X_test.reshape(n_samples_test, -1)
        else:
            X_train_reshaped = X_train
            X_valid_reshaped = X_valid
            X_test_reshaped = X_test
        
        if args.dim_reducer == "pca":
            # Use PCA-specific parameter
            dim_reducer = PCAdimReducer(n_components=args.pca_components)
            X_train_reduced = dim_reducer.fit_transform(X_train_reshaped)
            X_valid_reduced = dim_reducer.transform(X_valid_reshaped)
            X_test_reduced = dim_reducer.transform(X_test_reshaped)
            
            print(f"Reduced dimensions from {X_train_reshaped.shape[1]} to {X_train_reduced.shape[1]}")
            
        elif args.dim_reducer == "lda":
            # Check if PCA preprocessing is requested before LDA
            if args.pca_before_lda and X_train_reshaped.shape[1] > 500:
                print("Applying PCA preprocessing before LDA...")
                
                # Determine number of components for PCA
                n_classes = len(class_names)
                n_features = X_train_reshaped.shape[1]
                
                if args.pca_for_lda_components is not None:
                    pca_n_components = min(n_features, args.pca_for_lda_components)
                else:
                    # Default: use enough components to capture class information
                    pca_n_components = min(n_features, max(500, n_classes * 10))
                
                print(f"Using {pca_n_components} components for PCA preprocessing")
                
                # Apply PCA first
                pca_preprocessor = PCAdimReducer(n_components=pca_n_components)
                X_train_pca = pca_preprocessor.fit_transform(X_train_reshaped)
                X_valid_pca = pca_preprocessor.transform(X_valid_reshaped)
                X_test_pca = pca_preprocessor.transform(X_test_reshaped)
                
                print(f"PCA preprocessing: {X_train_reshaped.shape[1]} → {X_train_pca.shape[1]} dimensions")
                
                # Then apply LDA on PCA-reduced data
                n_components = args.lda_components
                
                # If n_components is None, use n_classes-1 as default
                if n_components is None:
                    n_components = len(class_names) - 1
                    print(f"Using default n_components={n_components} for LDA")
                
                # Ensure n_components doesn't exceed n_classes-1
                max_components = len(class_names) - 1
                if n_components > max_components:
                    print(f"Warning: LDA components {n_components} exceeds maximum allowed ({max_components}). Adjusting.")
                    n_components = max_components
                
                lda_reducer = LDAdimReducer(n_components=n_components)
                X_train_reduced = lda_reducer.fit_transform(X_train_pca, y_train)
                X_valid_reduced = lda_reducer.transform(X_valid_pca)
                X_test_reduced = lda_reducer.transform(X_test_pca)
                
                print(f"LDA: {X_train_pca.shape[1]} → {X_train_reduced.shape[1]} dimensions")
                print(f"Total reduction: {X_train_reshaped.shape[1]} → {X_train_reduced.shape[1]} dimensions")
            else:
                # Use LDA-specific parameter without PCA preprocessing
                n_components = args.lda_components
                
                # If n_components is None, use n_classes-1 as default
                if n_components is None:
                    n_components = len(class_names) - 1
                    print(f"Using default n_components={n_components} for LDA")
                
                # Ensure n_components doesn't exceed n_classes-1
                max_components = len(class_names) - 1
                if n_components > max_components:
                    print(f"Warning: LDA components {n_components} exceeds maximum allowed ({max_components}). Adjusting.")
                    n_components = max_components
                
                lda_reducer = LDAdimReducer(n_components=n_components)
                X_train_reduced = lda_reducer.fit_transform(X_train_reshaped, y_train)
                X_valid_reduced = lda_reducer.transform(X_valid_reshaped)
                X_test_reduced = lda_reducer.transform(X_test_reshaped)
                
                print(f"Reduced dimensions from {X_train_reshaped.shape[1]} to {X_train_reduced.shape[1]}")
            
        X_train, X_valid, X_test = X_train_reduced, X_valid_reduced, X_test_reduced
    
    # Create classifier
    if args.classifier == "knn":
        classifier = KNNClassifier(n_neighbors=args.n_neighbors)
    elif args.classifier == "svm":
        classifier = SVMClassifier(kernel=args.kernel)
    elif args.classifier == "cnn":
        classifier = CNNClassifier()
    elif args.classifier == "dbscan":
        classifier = DBSCANClassifier(min_samples=args.min_samples_per_subclass, auto_eps=True)
    
    # Apply subclassification if specified
    if args.use_subclasses:
        print("Using subclassification approach...")
        
        # Store original X_train for clustering
        X_for_clustering = X_train
        
        # If dimensionality reduction has been applied, consider using original space for clustering
        if args.dim_reducer != "none":
            print("Using original feature space for clustering to preserve class structure")
            if len(data['X_train'].shape) > 2:
                # IMPORTANT: We need to ensure that X_for_clustering has the same number of samples as y_train
                # If data augmentation was applied, we can't use the original data directly
                if args.augment or args.balance_classes:
                    print("Data augmentation was applied - using current feature space for clustering instead of original")
                    # Reshape current data to 2D if needed
                    if len(X_train.shape) > 2:
                        n_samples = X_train.shape[0]
                        X_for_clustering = X_train.reshape(n_samples, -1)
                else:
                    # No augmentation, safe to use original data
                    n_samples = data['X_train'].shape[0]
                    X_for_clustering = data['X_train'].reshape(n_samples, -1).astype(np.float32) / 255.0
        
        # Create subclasses from training data
        X_train_sub, y_train_sub, subclass_to_original = create_subclasses(
            X_for_clustering, y_train, 
            args.min_subclasses, 
            args.max_subclasses, 
            args.min_samples_per_subclass
        )
        
        # Train classifier on subclass data
        print(f"Training {args.classifier.upper()} classifier on subclass data...")
        classifier.fit(X_train, y_train_sub)
        
        # Evaluate on validation set
        print("Evaluating on validation set...")
        y_valid_subclass_pred = classifier.predict(X_valid)
        
        # Map subclass predictions back to original classes
        y_valid_pred = map_predictions_to_original(y_valid_subclass_pred, subclass_to_original)
        
        val_accuracy = accuracy_score(y_valid, y_valid_pred)
        print(f"Validation accuracy: {val_accuracy:.4f}")
        print("\nValidation report:")
        print(classification_report(y_valid, y_valid_pred, target_names=class_names))
        
        # Evaluate on test set
        print("Evaluating on test set...")
        y_test_subclass_pred = classifier.predict(X_test)
        
        # Map subclass predictions back to original classes
        y_test_pred = map_predictions_to_original(y_test_subclass_pred, subclass_to_original)
        
        test_accuracy = accuracy_score(y_test, y_test_pred)
        print(f"Test accuracy: {test_accuracy:.4f}")
        print("\nTest report:")
        print(classification_report(y_test, y_test_pred, target_names=class_names))
        
    else:
        # Train classifier on original classes
        print(f"Training {args.classifier.upper()} classifier...")
        classifier.fit(X_train, y_train)
        
        # Evaluate on validation set
        print("Evaluating on validation set...")
        y_valid_pred = classifier.predict(X_valid)
        val_accuracy = accuracy_score(y_valid, y_valid_pred)
        
        print(f"Validation accuracy: {val_accuracy:.4f}")
        print("\nValidation report:")
        print(classification_report(y_valid, y_valid_pred, target_names=class_names))
        
        # Evaluate on test set
        print("Evaluating on test set...")
        y_test_pred = classifier.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_test_pred)
        
        print(f"Test accuracy: {test_accuracy:.4f}")
        print("\nTest report:")
        print(classification_report(y_test, y_test_pred, target_names=class_names))

if __name__ == "__main__":
    main()
