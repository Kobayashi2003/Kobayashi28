import os
import pickle
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier

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
    # Use existing augmented data if available
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
        
        # Augment training set
        X_train, y_train = augment_dataset(X_train, y_train, augment_factor, use_knn_style=False)
        
        # Save augmented data
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
    features_train_filename = os.path.join(temp_dir, "train_svm_features.pkl")
    features_valid_filename = os.path.join(temp_dir, "valid_svm_features.pkl")
    features_test_filename = os.path.join(temp_dir, "test_svm_features.pkl")
    
    X_train_features = extract_features(X_train, 'train_svm', features_train_filename, n_jobs, use_knn_style=False)
    X_valid_features = extract_features(X_valid, 'valid_svm', features_valid_filename, n_jobs, use_knn_style=False)
    X_test_features = extract_features(X_test, 'test_svm', features_test_filename, n_jobs, use_knn_style=False)
    print(f"Extracted features: {X_train_features.shape[1]} features per image.")
    
    return X_train_features, X_valid_features, X_test_features

def reduce_dimensions(X_train_features, X_valid_features, X_test_features):
    # Feature preprocessing
    print("Preprocessing features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_features)
    X_valid_scaled = scaler.transform(X_valid_features)
    X_test_scaled = scaler.transform(X_test_features)
    
    # Apply PCA for dimensionality reduction
    print("Applying PCA...")
    n_components = min(X_train_scaled.shape[0], X_train_scaled.shape[1], 500)  # Cap max components
    # n_components = None
    pca = PCA(n_components=n_components)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_valid_pca = pca.transform(X_valid_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    
    print(f"PCA reduced dimensions: {X_train_scaled.shape[1]} → {X_train_pca.shape[1]}")
    print(f"Explained variance: {sum(pca.explained_variance_ratio_):.4f}")
    
    return X_train_pca, X_valid_pca, X_test_pca, scaler, pca

def train_or_load_model(X_train_pca, y_train, output_dir, use_svc):
    # Check if model already exists to avoid retraining
    model_path = os.path.join(output_dir, "svm_model.pkl")
    if os.path.exists(model_path):
        print(f"Loading existing SVM model from {model_path}")
        try:
            with open(model_path, 'rb') as f:
                svm_model = pickle.load(f)
            return svm_model
        except Exception as e:
            print(f"Error loading model: {e}. Training new model...")
    
    # Train SVM model with RBF kernel - good for high-dimensional data
    print("Training SVM model...")
    
    if use_svc:
        # Option 1: SVC with RBF kernel - good for non-linear data
        print("Using SVC with RBF kernel...")
        svm = SVC(C=10, kernel='rbf', gamma='scale', probability=True, 
                 class_weight='balanced', cache_size=2000, verbose=True)
    else:
        # Option 2: SGDClassifier with hinge loss (linear SVM) for multi-core processing
        print("Using SGDClassifier (linear SVM) with multi-core processing...")
        svm = SGDClassifier(loss='hinge', penalty='l2', alpha=0.001, 
                           class_weight='balanced', max_iter=1000, tol=1e-3,
                           n_jobs=-1, verbose=1)
    
    # Train on PCA-transformed data
    svm.fit(X_train_pca, y_train)
    
    # Save the model
    try:
        with open(model_path, 'wb') as f:
            pickle.dump(svm, f)
        print(f"Model saved to {model_path}")
    except Exception as e:
        print(f"Error saving model: {e}")
    
    return svm

def evaluate_model(svm, X_valid_pca, X_test_pca, X_test, y_valid, y_test, class_names, output_dir):
    # Evaluate on validation set
    print("Evaluating on validation set...")
    y_valid_pred = svm.predict(X_valid_pca)
    val_accuracy = accuracy_score(y_valid, y_valid_pred)
    print(f"Validation accuracy: {val_accuracy:.4f}")
    print(classification_report(y_valid, y_valid_pred, target_names=class_names, zero_division=0))
    
    # Evaluate on test set
    print("Evaluating on test set...")
    y_test_pred = svm.predict(X_test_pca)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(classification_report(y_test, y_test_pred, target_names=class_names, zero_division=0))
    
    # Save error analysis
    save_error_analysis(X_test, y_test, y_test_pred, class_names, output_dir, "test", "svm")
    
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
    img_size = (320, 320)  # Reduced size for faster processing

    output_dir = "../output/svm"
    n_jobs = None
    augment_factor = 5

    use_svc = True  # Set to True to use SVC, False to use SGDClassifier
    
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
    X_train_pca, X_valid_pca, X_test_pca, scaler, pca = reduce_dimensions(
        X_train_features, X_valid_features, X_test_features
    )
    
    # Train or load model
    svm = train_or_load_model(X_train_pca, y_train, output_dir, use_svc)
    
    # Evaluate model
    y_valid_pred, y_test_pred, val_accuracy, test_accuracy, class_accuracies = evaluate_model(
        svm, X_valid_pca, X_test_pca, X_test, y_valid, y_test, class_names, output_dir
    )
    
    print(f"SVM analysis complete. Results saved in {output_dir}.")

if __name__ == "__main__":
    main()