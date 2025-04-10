import numpy as np
import matplotlib.pyplot as plt
from data_utils import load_data
from pca import PCA
from lda import LDA
from knn import KNN

def run_experiment():
    """
    Run the face recognition experiment comparing PCA and LDA
    with KNN classification on the Yale dataset
    """
    # 1. Data loading
    X_train, y_train, X_test, y_test = load_data("Yale_64x64.mat", train_split=9)
    print(f"Dataset info: Training set {X_train.shape}, Test set {X_test.shape}")
    print(f"Number of classes: {len(np.unique(y_train))}")
    
    # Try different dimensions for dimensionality reduction
    # n_components_range = [2, 4, 8, 16, 32, 64]
    n_components_range = [32]
    pca_accuracies = []
    lda_accuracies = []
    
    # Test performance with different dimensions
    for n_comp in n_components_range:
        # 2. PCA dimensionality reduction
        pca = PCA(n_components=n_comp)
        pca.fit(X_train)
        X_train_pca = pca.transform(X_train)
        X_test_pca = pca.transform(X_test)
        
        # Adjust LDA dimension to not exceed (number of classes - 1)
        lda_n_comp = min(n_comp, len(np.unique(y_train)) - 1)
        
        # 3. LDA dimensionality reduction
        lda = LDA(n_components=lda_n_comp)
        lda.fit(X_train, y_train)
        X_train_lda = lda.transform(X_train)
        X_test_lda = lda.transform(X_test)
        
        # 4. KNN classification
        knn = KNN(k=3)
        
        # PCA + KNN
        knn.fit(X_train_pca, y_train)
        acc_pca = knn.score(X_test_pca, y_test)
        pca_accuracies.append(acc_pca)
        
        # LDA + KNN
        knn.fit(X_train_lda, y_train)
        acc_lda = knn.score(X_test_lda, y_test)
        lda_accuracies.append(acc_lda)
        
        print(f"Dimension {n_comp} - PCA+KNN accuracy: {acc_pca:.4f}, LDA+KNN accuracy: {acc_lda:.4f}")
    
    # Output best results
    best_pca_idx = np.argmax(pca_accuracies)
    best_lda_idx = np.argmax(lda_accuracies)
    print(f"Best PCA dimension: {n_components_range[best_pca_idx]}, Accuracy: {pca_accuracies[best_pca_idx]:.4f}")
    print(f"Best LDA dimension: {n_components_range[best_lda_idx]}, Accuracy: {lda_accuracies[best_lda_idx]:.4f}")
    
    # 5. Visualization with the best dimensions
    visualize_results(X_train, y_train, n_components_range, pca_accuracies, lda_accuracies)

def visualize_results(X_train, y_train, dimensions, pca_accuracies, lda_accuracies):
    """
    Visualize the experiment results
    
    Parameters:
    -----------
    X_train : array-like, shape (n_samples, n_features)
        Training data
    y_train : array-like, shape (n_samples,)
        Training labels
    dimensions : list
        List of dimensions used in the experiment
    pca_accuracies : list
        Accuracies for PCA+KNN for each dimension
    lda_accuracies : list
        Accuracies for LDA+KNN for each dimension
    """
    plt.figure(figsize=(15, 10))
    
    # Accuracy vs. dimension plot
    plt.subplot(2, 2, 1)
    plt.plot(dimensions, pca_accuracies, 'o-', label='PCA+KNN')
    plt.plot(dimensions, lda_accuracies, 's-', label='LDA+KNN')
    plt.xlabel('Dimension')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Classification Accuracy with Different Dimensions')
    plt.grid(True)
    
    # PCA 2D visualization
    plt.subplot(2, 2, 3)
    pca_vis = PCA(n_components=2)
    pca_vis.fit(X_train)
    X_vis_pca = pca_vis.transform(X_train)
    plt.scatter(X_vis_pca[:, 0], X_vis_pca[:, 1], c=y_train, cmap='tab20', alpha=0.6)
    plt.title("PCA 2D Projection")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar(label='Class')
    
    # LDA 2D visualization
    plt.subplot(2, 2, 4)
    n_classes = len(np.unique(y_train))
    lda_vis = LDA(n_components=min(2, n_classes-1))
    lda_vis.fit(X_train, y_train)
    X_vis_lda = lda_vis.transform(X_train)
    
    # Handle the case when LDA has only 1 component
    if X_vis_lda.shape[1] > 1:
        plt.scatter(X_vis_lda[:, 0], X_vis_lda[:, 1], c=y_train, cmap='tab20', alpha=0.6)
        plt.ylabel("LD2")
    else:
        plt.scatter(X_vis_lda[:, 0], np.zeros_like(X_vis_lda[:, 0]), c=y_train, cmap='tab20', alpha=0.6)
        plt.ylabel("Sample index")
        
    plt.title("LDA 2D Projection")
    plt.xlabel("LD1")
    plt.colorbar(label='Class')
    
    plt.tight_layout()
    plt.show()
    plt.savefig('result.png')

if __name__ == "__main__":
    run_experiment() 