import numpy as np
import matplotlib.pyplot as plt
import os
from utils import load_data
from pca import PCA as CustomPCA
from lda import LDA as CustomLDA
from knn import KNN as CustomKNN
from sklearn.decomposition import PCA as SklearnPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as SklearnLDA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def visualize_eigenvectors(X_train, y_train, img_shape=(64, 64)):
    """
    Visualize the first 8 eigenvectors (components) of PCA and LDA as facial images
    
    Parameters:
    -----------
    X_train : array-like, shape (n_samples, n_features)
        Training data
    y_train : array-like, shape (n_samples,)
        Training labels
    img_shape : tuple
        Original shape of the images (height, width)
    """
    # Create models with at least 8 components
    n_components = 8
    
    # Fit PCA model
    pca_model = CustomPCA(n_components=n_components)
    pca_model.fit(X_train)
    
    # Fit LDA model (using SVD implementation)
    lda_model = CustomLDA(n_components=min(n_components, len(np.unique(y_train))-1))
    lda_model.fit_svd(X_train, y_train)
    
    # Visualize PCA eigenvectors
    plt.figure(figsize=(16, 4))
    plt.suptitle("PCA Eigenfaces", fontsize=16)
    
    for i in range(n_components):
        plt.subplot(2, 4, i+1)
        # Get the component and reshape to image dimensions
        component = pca_model.get_component(i).reshape(img_shape)
        
        # Normalize for better visualization
        component = (component - component.min()) / (component.max() - component.min())
        
        plt.imshow(component, cmap='gray')
        plt.title(f"Eigenface {i+1}")
        plt.axis('off')
    
    plt.tight_layout()
    os.makedirs('../images', exist_ok=True)
    plt.savefig('../images/pca_eigenfaces.png')
    plt.close()
    
    # Visualize LDA components
    # For LDA, the number of components is limited by number of classes - 1
    lda_n_components = lda_model.W.shape[1]
    
    plt.figure(figsize=(16, 4))
    plt.suptitle("LDA Fisherfaces", fontsize=16)
    
    for i in range(min(n_components, lda_n_components)):
        plt.subplot(2, 4, i+1)
        # Get the component and reshape to image dimensions
        component = lda_model.get_component(i).reshape(img_shape)
        
        # Normalize for better visualization
        component = (component - component.min()) / (component.max() - component.min())
        
        plt.imshow(component, cmap='gray')
        plt.title(f"Fisherface {i+1}")
        plt.axis('off')
    
    plt.tight_layout()
    os.makedirs('../images', exist_ok=True)
    plt.savefig('../images/lda_fisherfaces.png')
    plt.close()

def run_custom_experiment(X_train, y_train, X_test, y_test, n_components_range):
    """
    Run the face recognition experiment using custom implementations
    
    Parameters:
    -----------
    X_train, y_train : Training data and labels
    X_test, y_test : Test data and labels
    n_components_range : List of dimensions to test
    
    Returns:
    --------
    pca_accuracies, lda_accuracies : Lists of accuracies for each dimension
    """
    pca_accuracies = []
    lda_accuracies = []
    
    for n_comp in n_components_range:
        # PCA dimensionality reduction
        pca = CustomPCA(n_components=n_comp)
        pca.fit(X_train)
        X_train_pca = pca.transform(X_train)
        X_test_pca = pca.transform(X_test)
        
        # Adjust LDA dimension to not exceed (number of classes - 1)
        lda_n_comp = min(n_comp, len(np.unique(y_train)) - 1)
        
        # LDA dimensionality reduction (using SVD implementation only)
        lda = CustomLDA(n_components=lda_n_comp)
        lda.fit_svd(X_train, y_train)
        X_train_lda = lda.transform(X_train)
        X_test_lda = lda.transform(X_test)
        
        # KNN classification
        knn = CustomKNN(k=3)
        
        # PCA + KNN
        knn.fit(X_train_pca, y_train)
        acc_pca = knn.score(X_test_pca, y_test)
        pca_accuracies.append(acc_pca)
        
        # LDA + KNN
        knn.fit(X_train_lda, y_train)
        acc_lda = knn.score(X_test_lda, y_test)
        lda_accuracies.append(acc_lda)
        
        print(f"Dimension {n_comp} - Custom PCA+KNN accuracy: {acc_pca:.4f}, Custom LDA+KNN accuracy: {acc_lda:.4f}")
    
    return pca_accuracies, lda_accuracies

def run_sklearn_experiment(X_train, y_train, X_test, y_test, n_components_range):
    """
    Run the face recognition experiment using sklearn implementations
    
    Parameters:
    -----------
    X_train, y_train : Training data and labels
    X_test, y_test : Test data and labels
    n_components_range : List of dimensions to test
    
    Returns:
    --------
    pca_accuracies, lda_accuracies : Lists of accuracies for each dimension
    """
    pca_accuracies = []
    lda_accuracies = []
    
    for n_comp in n_components_range:
        # PCA dimensionality reduction
        pca = SklearnPCA(n_components=n_comp)
        X_train_pca = pca.fit_transform(X_train)
        X_test_pca = pca.transform(X_test)
        
        # Adjust LDA dimension to not exceed (number of classes - 1)
        lda_n_comp = min(n_comp, len(np.unique(y_train)) - 1)
        
        # LDA dimensionality reduction
        lda = SklearnLDA(n_components=lda_n_comp)
        X_train_lda = lda.fit_transform(X_train, y_train)
        X_test_lda = lda.transform(X_test)
        
        # KNN classification
        knn = KNeighborsClassifier(n_neighbors=3)
        
        # PCA + KNN
        knn.fit(X_train_pca, y_train)
        acc_pca = knn.score(X_test_pca, y_test)
        pca_accuracies.append(acc_pca)
        
        # LDA + KNN
        knn.fit(X_train_lda, y_train)
        acc_lda = knn.score(X_test_lda, y_test)
        lda_accuracies.append(acc_lda)
        
        print(f"Dimension {n_comp} - Sklearn PCA+KNN accuracy: {acc_pca:.4f}, Sklearn LDA+KNN accuracy: {acc_lda:.4f}")
    
    return pca_accuracies, lda_accuracies

def run_comparison_experiment(X_train, y_train, X_test, y_test, n_components_range):
    """
    Compare custom implementations with scikit-learn's implementations
    
    Parameters:
    -----------
    X_train, y_train : Training data and labels
    X_test, y_test : Test data and labels
    n_components_range : List of dimensions to test
    
    Returns:
    --------
    results : Dictionary containing comparison results
    """
    results = {
        'dimensions': n_components_range,
        'custom_pca': [],
        'sklearn_pca': [],
        'custom_lda': [],
        'sklearn_lda': []
    }
    
    for n_comp in n_components_range:
        print(f"\nTesting with {n_comp} components:")
        
        # ---- PCA Comparison ----
        # Custom PCA
        custom_pca = CustomPCA(n_components=n_comp)
        custom_pca.fit(X_train)
        X_train_custom_pca = custom_pca.transform(X_train)
        X_test_custom_pca = custom_pca.transform(X_test)
        
        # Sklearn PCA
        sklearn_pca = SklearnPCA(n_components=n_comp)
        X_train_sklearn_pca = sklearn_pca.fit_transform(X_train)
        X_test_sklearn_pca = sklearn_pca.transform(X_test)
        
        # ---- LDA Comparison ----
        # Adjust LDA dimension to not exceed (number of classes - 1)
        lda_n_comp = min(n_comp, len(np.unique(y_train)) - 1)
        
        # Custom LDA (using SVD implementation only)
        custom_lda = CustomLDA(n_components=lda_n_comp)
        custom_lda.fit_svd(X_train, y_train)
        X_train_custom_lda = custom_lda.transform(X_train)
        X_test_custom_lda = custom_lda.transform(X_test)
        
        # Sklearn LDA
        sklearn_lda = SklearnLDA(n_components=lda_n_comp)
        X_train_sklearn_lda = sklearn_lda.fit_transform(X_train, y_train)
        X_test_sklearn_lda = sklearn_lda.transform(X_test)
        
        # ---- Classification and Evaluation ----
        # Custom KNN for custom implementations
        custom_knn = CustomKNN(k=3)
        
        # Sklearn KNN for sklearn implementations
        sklearn_knn = KNeighborsClassifier(n_neighbors=3)
        
        # PCA+KNN with custom implementation
        custom_knn.fit(X_train_custom_pca, y_train)
        custom_pca_pred = custom_knn.predict(X_test_custom_pca)
        custom_pca_acc = accuracy_score(y_test, custom_pca_pred)
        results['custom_pca'].append(custom_pca_acc)
        
        # PCA+KNN with sklearn
        sklearn_knn.fit(X_train_sklearn_pca, y_train)
        sklearn_pca_pred = sklearn_knn.predict(X_test_sklearn_pca)
        sklearn_pca_acc = accuracy_score(y_test, sklearn_pca_pred)
        results['sklearn_pca'].append(sklearn_pca_acc)
        
        # LDA+KNN with custom implementation
        custom_knn.fit(X_train_custom_lda, y_train)
        custom_lda_pred = custom_knn.predict(X_test_custom_lda)
        custom_lda_acc = accuracy_score(y_test, custom_lda_pred)
        results['custom_lda'].append(custom_lda_acc)
        
        # LDA+KNN with sklearn
        sklearn_knn.fit(X_train_sklearn_lda, y_train)
        sklearn_lda_pred = sklearn_knn.predict(X_test_sklearn_lda)
        sklearn_lda_acc = accuracy_score(y_test, sklearn_lda_pred)
        results['sklearn_lda'].append(sklearn_lda_acc)
        
        print(f"PCA+KNN - Custom: {custom_pca_acc:.4f}, Sklearn: {sklearn_pca_acc:.4f}")
        print(f"LDA+KNN - Custom: {custom_lda_acc:.4f}, Sklearn: {sklearn_lda_acc:.4f}")
    
    return results

def visualize_custom_results(X_train, y_train, dimensions, pca_accuracies, lda_accuracies):
    """
    Visualize results from custom implementations
    """
    plt.figure(figsize=(15, 10))
    
    # Accuracy vs. dimension plot
    plt.subplot(2, 2, 1)
    plt.plot(dimensions, pca_accuracies, 'o-', label='PCA+KNN')
    plt.plot(dimensions, lda_accuracies, 's-', label='LDA+KNN')
    plt.xlabel('Dimension')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Classification Accuracy with Different Dimensions (Custom)')
    plt.grid(True)
    
    # PCA 2D visualization
    plt.subplot(2, 2, 3)
    pca_vis = CustomPCA(n_components=2)
    pca_vis.fit(X_train)
    X_vis_pca = pca_vis.transform(X_train)
    plt.scatter(X_vis_pca[:, 0], X_vis_pca[:, 1], c=y_train, cmap='tab20', alpha=0.6)
    plt.title("PCA 2D Projection (Custom)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar(label='Class')
    
    # LDA 2D visualization
    plt.subplot(2, 2, 4)
    n_classes = len(np.unique(y_train))
    lda_vis = CustomLDA(n_components=min(2, n_classes-1))
    # Only use SVD-based LDA implementation
    lda_vis.fit_svd(X_train, y_train)
    X_vis_lda = lda_vis.transform(X_train)
    plt.scatter(X_vis_lda[:, 0], X_vis_lda[:, 1], c=y_train, cmap='tab20', alpha=0.6)
    plt.title("LDA 2D Projection (Custom)")
    plt.xlabel("LD1")
    plt.ylabel("LD2")
    plt.colorbar(label='Class')
    
    plt.tight_layout()
    
    # Save the figure
    os.makedirs('../images', exist_ok=True)
    plt.savefig(f'../images/custom_results.png')
    plt.close()

def visualize_sklearn_results(X_train, y_train, dimensions, pca_accuracies, lda_accuracies):
    """
    Visualize results from sklearn implementations
    """
    plt.figure(figsize=(15, 10))
    
    # Accuracy vs. dimension plot
    plt.subplot(2, 2, 1)
    plt.plot(dimensions, pca_accuracies, 'o-', label='PCA+KNN')
    plt.plot(dimensions, lda_accuracies, 's-', label='LDA+KNN')
    plt.xlabel('Dimension')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Classification Accuracy with Different Dimensions (sklearn)')
    plt.grid(True)
    
    # PCA 2D visualization
    plt.subplot(2, 2, 3)
    pca_vis = SklearnPCA(n_components=2)
    X_vis_pca = pca_vis.fit_transform(X_train)
    plt.scatter(X_vis_pca[:, 0], X_vis_pca[:, 1], c=y_train, cmap='tab20', alpha=0.6)
    plt.title("PCA 2D Projection (sklearn)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar(label='Class')
    
    # LDA 2D visualization
    plt.subplot(2, 2, 4)
    n_classes = len(np.unique(y_train))
    lda_vis = SklearnLDA(n_components=min(2, n_classes-1))
    X_vis_lda = lda_vis.fit_transform(X_train, y_train)
    plt.scatter(X_vis_lda[:, 0], X_vis_lda[:, 1], c=y_train, cmap='tab20', alpha=0.6)
    plt.title("LDA 2D Projection (sklearn)")
    plt.xlabel("LD1")
    plt.ylabel("LD2")
    plt.colorbar(label='Class')
    
    plt.tight_layout()
    
    # Save the figure
    os.makedirs('../images', exist_ok=True)
    plt.savefig('../images/sklearn_results.png')
    plt.close()

def visualize_comparison(results):
    """
    Visualize comparison between custom and sklearn implementations
    """
    plt.figure(figsize=(12, 10))
    
    # PCA comparison
    plt.subplot(2, 1, 1)
    plt.plot(results['dimensions'], results['custom_pca'], 'o-', label='Custom PCA+KNN')
    plt.plot(results['dimensions'], results['sklearn_pca'], 's-', label='Sklearn PCA+KNN')
    plt.xlabel('Number of Components')
    plt.ylabel('Accuracy')
    plt.title('PCA Implementation Comparison')
    plt.legend()
    plt.grid(True)
    
    # LDA comparison
    plt.subplot(2, 1, 2)
    plt.plot(results['dimensions'], results['custom_lda'], 'o-', label='Custom LDA+KNN')
    plt.plot(results['dimensions'], results['sklearn_lda'], 's-', label='Sklearn LDA+KNN')
    plt.xlabel('Number of Components')
    plt.ylabel('Accuracy')
    plt.title('LDA Implementation Comparison')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    # Save the figure
    os.makedirs('../images', exist_ok=True)
    plt.savefig('../images/implementation_comparison.png')
    plt.close()

def run_all_experiments():
    """Run all experiments: custom, sklearn, and comparison"""
    print("=== Running Face Recognition Experiments ===")
    
    # Load data once for all experiments
    X_train, y_train, X_test, y_test = load_data("../data/Yale_64x64.mat", train_split=9)
    print(f"Dataset info: Training set {X_train.shape}, Test set {X_test.shape}")
    print(f"Number of classes: {len(np.unique(y_train))}")
    
    # Visualize PCA and LDA components as facial images (eigenfaces/fisherfaces)
    print("\n=== Visualizing PCA and LDA components as faces ===")
    # Get the original image dimensions from the dataset
    img_shape = (64, 64)  # Yale dataset images are 64x64
    visualize_eigenvectors(X_train, y_train, img_shape)
    
    # Define dimensions to test
    n_components_range = [2, 4, 8, 16, 32, 64]
    
    print("\n=== Running Custom Implementation Experiment ===")
    custom_pca_acc, custom_lda_acc = run_custom_experiment(
        X_train, y_train, X_test, y_test, n_components_range)
    visualize_custom_results(
        X_train, y_train, n_components_range, custom_pca_acc, custom_lda_acc)
    
    print("\n=== Running Sklearn Implementation Experiment ===")
    sklearn_pca_acc, sklearn_lda_acc = run_sklearn_experiment(
        X_train, y_train, X_test, y_test, n_components_range)
    visualize_sklearn_results(
        X_train, y_train, n_components_range, sklearn_pca_acc, sklearn_lda_acc)
    
    print("\n=== Running Implementation Comparison Experiment ===")
    comparison_results = run_comparison_experiment(
        X_train, y_train, X_test, y_test, n_components_range)
    visualize_comparison(comparison_results)
    
    print("\n=== All experiments completed successfully ===")
    print(f"Results saved to ../images/")

if __name__ == "__main__":
    run_all_experiments() 