import os
import pickle

import numpy as np

from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.feature_selection import SelectKBest, f_classif

from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import classification_report, accuracy_score


from utils import (
    load_dataset, 
    extract_features, 
    augment_dataset, 
    check_for_augmented_data, 
    save_augmented_data, 
    save_error_analysis
)

def prepare_dataset(data_dir, img_size, temp_dir, augment_factor):
    # Check for existing augmented data
    augmented_data_filename = os.path.join(temp_dir, f"augmented_data_{img_size[0]}x{img_size[1]}.pkl")
    augmented_data = check_for_augmented_data(augmented_data_filename)
    
    if augmented_data is not None:
        X_train = augmented_data['X_train']
        y_train = augmented_data['y_train']
        X_valid = augmented_data['X_valid']
        y_valid = augmented_data['y_valid']
        X_test = augmented_data['X_test']
        y_test = augmented_data['y_test']
        class_names = augmented_data['class_names']
        print(f"Using existing augmented dataset with {len(X_train)} training samples.")
    else:
        # Load dataset
        print("Loading dataset...")
        data = load_dataset(data_dir, img_size=img_size)
        X_train, y_train = data['X_train'], data['y_train']
        X_valid, y_valid = data['X_valid'], data['y_valid']
        X_test, y_test = data['X_test'], data['y_test']
        class_names = data['class_names']
        print(f"Dataset loaded: {len(X_train)} train, {len(X_valid)} valid, {len(X_test)} test samples.")
        
        # Apply data augmentation
        X_train, y_train = augment_dataset(X_train, y_train, augment_factor, use_knn_style=True)
        
        # Save augmented data for future use
        augmented_data = {
            'X_train': X_train, 'y_train': y_train,
            'X_valid': X_valid, 'y_valid': y_valid,
            'X_test': X_test, 'y_test': y_test,
            'class_names': class_names
        }
        save_augmented_data(augmented_data, augmented_data_filename)
    
    return X_train, y_train, X_valid, y_valid, X_test, y_test, class_names

def process_features(X_train, X_valid, X_test, temp_dir, n_jobs):
    # Extract features
    print("Extracting features...")
    features_train_filename = os.path.join(temp_dir, "train_knn_features.pkl")
    features_valid_filename = os.path.join(temp_dir, "valid_knn_features.pkl")
    features_test_filename = os.path.join(temp_dir, "test_knn_features.pkl")
    
    X_train_features = extract_features(X_train, 'train_knn', features_train_filename, n_jobs, use_knn_style=True)
    X_valid_features = extract_features(X_valid, 'valid_knn', features_valid_filename, n_jobs, use_knn_style=True)
    X_test_features = extract_features(X_test, 'test_knn', features_test_filename, n_jobs, use_knn_style=True)
    print(f"Extracted {X_train_features.shape[1]} features per image.")
    
    return X_train_features, X_valid_features, X_test_features

def reduce_dimensions(X_train_features, X_valid_features, X_test_features, y_train, n_features=None):
    # Feature preprocessing
    print("Preprocessing features...")
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train_features)
    X_valid_scaled = scaler.transform(X_valid_features)
    X_test_scaled = scaler.transform(X_test_features)
    
    # Dimensionality reduction with PCA
    print("Applying PCA for dimensionality reduction...")
    n_components = min(X_train_scaled.shape[0], X_train_scaled.shape[1], 500)
    pca = PCA(n_components=n_components)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_valid_pca = pca.transform(X_valid_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    print(f"PCA reduced features: {X_train_scaled.shape[1]} → {X_train_pca.shape[1]}")
    print(f"Explained variance: {sum(pca.explained_variance_ratio_):.4f}")
    
    # Apply LDA for further supervised dimensionality reduction
    print("Applying LDA for better class separation...")
    n_components_lda = min(len(np.unique(y_train)) - 1, X_train_pca.shape[1])
    lda = LinearDiscriminantAnalysis(n_components=n_components_lda)
    X_train_lda = lda.fit_transform(X_train_pca, y_train)
    X_valid_lda = lda.transform(X_valid_pca)
    X_test_lda = lda.transform(X_test_pca)
    print(f"LDA reduced features: {X_train_pca.shape[1]} → {X_train_lda.shape[1]}")
    
    # Optional feature selection
    if n_features is not None and n_features < X_train_lda.shape[1]:
        print(f"Selecting top {n_features} features...")
        selector = SelectKBest(f_classif, k=n_features)
        X_train_selected = selector.fit_transform(X_train_lda, y_train)
        X_valid_selected = selector.transform(X_valid_lda)
        X_test_selected = selector.transform(X_test_lda)
        
        selected_indices = selector.get_support(indices=True)
        print(f"Using {len(selected_indices)} selected features")
    else:
        X_train_selected = X_train_lda
        X_valid_selected = X_valid_lda
        X_test_selected = X_test_lda
        selector = None
    
    return X_train_selected, X_valid_selected, X_test_selected, scaler, pca, lda, selector

def train_or_load_model(X_train_selected, y_train, X_valid_selected, y_valid, output_dir, class_names, scaler, pca, lda, selector):
    # Check if model already exists
    model_path = os.path.join(output_dir, "knn_model.pkl")
    if os.path.exists(model_path):
        print(f"Loading existing KNN model from {model_path}")
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
                knn_model = model_data['model']
            load_model_success = True
        except Exception as e:
            print(f"Error loading model: {e}. Training new model...")
            load_model_success = False
    else:
        load_model_success = False
    
    if not load_model_success:
        # Train KNN model
        print("Training KNN model...")
        n_neighbors = int(np.sqrt(len(X_train_selected)))
        print(f"Using {n_neighbors} neighbors based on dataset size")
        
        knn_model = KNeighborsClassifier(
            n_neighbors=n_neighbors,
            weights='distance',
            metric='minkowski',
            p=2,
            algorithm='auto',
            n_jobs=-1
        )
        
        knn_model.fit(X_train_selected, y_train)
        
        # Validate model
        y_valid_pred = knn_model.predict(X_valid_selected)
        valid_accuracy = accuracy_score(y_valid, y_valid_pred)
        print(f"Validation accuracy: {valid_accuracy:.4f}")
        
        # Save the model
        try:
            with open(model_path, 'wb') as f:
                pickle.dump({
                    'model': knn_model,
                    'selector': selector,
                    'pca': pca,
                    'lda': lda,
                    'scaler': scaler,
                    'class_names': class_names
                }, f)
            print(f"Model saved to {model_path}")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    return knn_model

def evaluate_model(knn_model, X_valid_selected, X_test_selected, X_test, y_valid, y_test, class_names, output_dir):
    # Evaluate on validation set
    print("Evaluating on validation set...")
    y_valid_pred = knn_model.predict(X_valid_selected)
    val_accuracy = accuracy_score(y_valid, y_valid_pred)
    print(f"Validation accuracy: {val_accuracy:.4f}")
    print(classification_report(y_valid, y_valid_pred, target_names=class_names, zero_division=0))
    
    # Evaluate on test set
    print("Evaluating on test set...")
    y_test_pred = knn_model.predict(X_test_selected)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(classification_report(y_test, y_test_pred, target_names=class_names, zero_division=0))
    
    # Save error analysis
    save_error_analysis(X_test, y_test, y_test_pred, class_names, output_dir, "test", "knn")
    
    # Calculate accuracy for each class
    class_accuracies = {}
    for cls_idx, cls_name in enumerate(class_names):
        cls_samples = (y_test == cls_idx)
        if np.sum(cls_samples) > 0:
            cls_acc = accuracy_score(y_test[cls_samples], y_test_pred[cls_samples])
            class_accuracies[cls_name] = cls_acc
    
    # Print class-wise accuracies
    print("\nAccuracy by rock type:")
    for cls_name, acc in sorted(class_accuracies.items(), key=lambda x: x[1]):
        print(f"{cls_name}: {acc:.4f}")
    
    return y_valid_pred, y_test_pred, val_accuracy, test_accuracy, class_accuracies

def main():
    # Configuration
    data_dir = "../data"
    img_size = (320, 320)

    output_dir = "../output/knn"
    n_jobs = None
    augment_factor = 10

    n_features = None  # Set to a number to enable feature selection
    
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare dataset
    X_train, y_train, X_valid, y_valid, X_test, y_test, class_names = prepare_dataset(
        data_dir, img_size, output_dir, augment_factor
    )
    
    # Process features
    X_train_features, X_valid_features, X_test_features = process_features(
        X_train, X_valid, X_test, output_dir, n_jobs
    )
    
    # Reduce dimensions
    X_train_selected, X_valid_selected, X_test_selected, scaler, pca, lda, selector = reduce_dimensions(
        X_train_features, X_valid_features, X_test_features, y_train, n_features
    )
    
    # Train or load model
    knn_model = train_or_load_model(
        X_train_selected, y_train, X_valid_selected, y_valid, output_dir, class_names, 
        scaler, pca, lda, selector
    )
    
    # Evaluate model
    y_valid_pred, y_test_pred, val_accuracy, test_accuracy, class_accuracies = evaluate_model(
        knn_model, X_valid_selected, X_test_selected, X_test, y_valid, y_test, class_names, output_dir
    )
    
    print(f"KNN analysis complete. Results saved in {output_dir}.")

if __name__ == "__main__":
    main()