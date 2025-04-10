import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import time
import glob
import cv2

# Import custom modules
from data_utils import load_data, load_image_data, standardize_features, extract_basic_features, extract_advanced_features
from knn import KNNClassifier
from lda import LDADimensionReducer
from pca import PCA
from svm import SVMClassifier
from cnn import CNNClassifier

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Rock Image Classification with dimensionality reduction')
    
    # Dataset arguments
    parser.add_argument('--data-dir', type=str, default='./RockData',
                       help='Path to the dataset directory')
    parser.add_argument('--use-augmented', action='store_true',
                       help='Use augmented dataset (if available)')
    
    # Feature extraction arguments
    parser.add_argument('--advanced-features', action='store_true',
                       help='Use advanced feature extraction (texture, color, shape)')
    
    # Classifier selection
    parser.add_argument('--classifier', type=str, choices=['knn', 'svm', 'cnn', 'all'], default='knn',
                       help='Classifier to use (knn, svm, cnn, or all)')
    
    # SVM-specific arguments
    parser.add_argument('--svm-strategy', type=str, choices=['standard', 'ovr', 'ovo', 'ensemble'], default='standard',
                        help='SVM multiclass strategy (standard, ovr, ovo, or ensemble)')
    
    # CNN-specific arguments
    parser.add_argument('--cnn-model', type=str, choices=['simple', 'resnet18', 'resnet50', 'efficientnet_b0'], 
                        default='resnet50', help='CNN model architecture')
    parser.add_argument('--cnn-epochs', type=int, default=10,
                        help='Number of training epochs for CNN')
    parser.add_argument('--cnn-batch-size', type=int, default=32,
                        help='Batch size for CNN training')
    parser.add_argument('--freeze-backbone', action='store_true',
                        help='Freeze backbone for transfer learning (CNN only)')
    
    # Dimensionality reduction arguments
    parser.add_argument('--dim-reduction', type=str, choices=['none', 'pca', 'lda', 'both'], default='none',
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
    
    # Setup paths
    if args.use_augmented and os.path.exists('./AugmentedRockData'):
        data_dir = './AugmentedRockData'
        print("Using augmented dataset")
    else:
        data_dir = args.data_dir
        print(f"Using dataset at {data_dir}")
    
    train_dir = os.path.join(data_dir, 'train')
    valid_dir = os.path.join(data_dir, 'valid')
    test_dir = os.path.join(data_dir, 'test')
    
    # Create output directory
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(args.output_dir, f"results_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get rock classes
    rock_classes = sorted([d for d in os.listdir(train_dir) 
                         if os.path.isdir(os.path.join(train_dir, d))])
    print(f"Rock types: {rock_classes}")
    print(f"Total classes: {len(rock_classes)}")
    
    # Check if running CNN classifier
    is_cnn = args.classifier in ['cnn', 'all']
    
    # For non-CNN classifiers, extract features
    if args.classifier in ['knn', 'svm', 'all']:
        # Select feature extractor
        if args.advanced_features:
            feature_extractor = extract_advanced_features
            print("Using advanced feature extraction")
        else:
            feature_extractor = extract_basic_features
            print("Using basic feature extraction")
        
        # Load and extract features
        print("\nLoading and extracting features...")
        X_train, y_train = load_data(train_dir, rock_classes, feature_extractor)
        X_valid, y_valid = load_data(valid_dir, rock_classes, feature_extractor)
        X_test, y_test = load_data(test_dir, rock_classes, feature_extractor)
        
        print(f"Training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
        print(f"Validation set: {X_valid.shape[0]} samples")
        print(f"Test set: {X_test.shape[0]} samples")
        
        # Standardize features
        print("\nStandardizing features...")
        (X_train_scaled, X_valid_scaled, X_test_scaled), scaler = standardize_features(
            X_train, X_valid, X_test)
        
        # Initialize dictionary to store data for each dimensionality reduction method
        reduction_data = {}
        
        # Apply PCA if requested
        if args.dim_reduction in ['pca', 'both']:
            pca_output_dir = os.path.join(output_dir, 'pca')
            os.makedirs(pca_output_dir, exist_ok=True)
            
            print("\nApplying PCA for dimensionality reduction...")
            # Create PCA model
            n_components = args.pca_components
            pca = PCA(n_components=n_components, output_dir=pca_output_dir)
            
            # Fit and transform data
            X_train_pca = pca.fit_transform(X_train_scaled)
            X_valid_pca = pca.transform(X_valid_scaled)
            X_test_pca = pca.transform(X_test_scaled)
            
            # Determine number of components to use (if not specified)
            if n_components is None:
                # Find number of components that explain 95% of variance
                cumulative_var = np.cumsum(pca.explained_variance_ratio)
                n_components = np.argmax(cumulative_var >= 0.95) + 1
                print(f"Using {n_components} PCA components (explains 95% of variance)")
                
                # Update data to use only these components
                X_train_pca = X_train_pca[:, :n_components]
                X_valid_pca = X_valid_pca[:, :n_components]
                X_test_pca = X_test_pca[:, :n_components]
            
            # Visualize PCA results
            pca.plot_explained_variance(max_components=min(50, len(pca.explained_variance)))
            pca.plot_2d_projection(X_train_scaled, y_train, class_names=rock_classes)
            
            # Store PCA-transformed data
            reduction_data['pca'] = {
                'train': X_train_pca,
                'valid': X_valid_pca,
                'test': X_test_pca,
                'name': 'PCA',
                'n_components': n_components
            }
            
            print(f"Data after PCA: {X_train_pca.shape[1]} features")
        
        # Apply LDA if requested
        if args.dim_reduction in ['lda', 'both']:
            lda_output_dir = os.path.join(output_dir, 'lda')
            os.makedirs(lda_output_dir, exist_ok=True)
            
            print("\nApplying LDA for dimensionality reduction...")
            # For LDA, number of components is limited by number of classes
            max_lda_components = min(len(rock_classes) - 1, X_train_scaled.shape[1])
            n_components = args.lda_components
            
            if n_components is None:
                n_components = max_lda_components
            else:
                n_components = min(n_components, max_lda_components)
            
            print(f"Using {n_components} LDA components")
            
            # Create and fit LDA model
            lda = LDADimensionReducer(output_dir=lda_output_dir)
            X_train_lda = lda.fit_transform(X_train_scaled, y_train, n_components)
            X_valid_lda = lda.transform(X_valid_scaled)
            X_test_lda = lda.transform(X_test_scaled)
            
            # Visualize LDA projection
            lda.visualize_projection(X_train_scaled, y_train, rock_classes)
            
            # Store LDA-transformed data
            reduction_data['lda'] = {
                'train': X_train_lda,
                'valid': X_valid_lda,
                'test': X_test_lda,
                'name': 'LDA',
                'n_components': n_components
            }
            
            print(f"Data after LDA: {X_train_lda.shape[1]} features")
        
        # Use raw standardized data if no dimensionality reduction requested
        if args.dim_reduction == 'none':
            reduction_data['none'] = {
                'train': X_train_scaled,
                'valid': X_valid_scaled,
                'test': X_test_scaled,
                'name': 'No Reduction',
                'n_components': X_train_scaled.shape[1]
            }
        
        # Train and evaluate models for each dimensionality reduction method
        results = {}
        
        for method, data in reduction_data.items():
            method_name = data['name']
            
            # Train and evaluate KNN if selected
            if args.classifier in ['knn', 'all']:
                knn_output_dir = os.path.join(output_dir, f'knn_{method}')
                os.makedirs(knn_output_dir, exist_ok=True)
                
                print("\n" + "="*60)
                print(f"KNN CLASSIFICATION WITH {method_name} DIMENSIONALITY REDUCTION")
                print(f"Number of features: {data['n_components']}")
                print("="*60)
                
                # Create and train KNN model
                knn = KNNClassifier(output_dir=knn_output_dir)
                
                if args.advanced_features:
                    print("\nTraining KNN with grid search...")
                    knn.train_advanced(data['train'], y_train)
                else:
                    print("\nTraining KNN with basic validation...")
                    knn.train_basic(data['train'], y_train, data['valid'], y_valid)
                
                # Evaluate KNN model
                knn_accuracy, _ = knn.evaluate(data['test'], y_test, rock_classes, f'_knn_{method}')
                
                # Save model
                knn.save_model(f'knn_model_{method}.pkl')
                
                results[f'knn_{method}'] = {
                    'accuracy': knn_accuracy,
                    'name': f'KNN with {method_name}',
                    'n_components': data['n_components'],
                    'classifier': 'KNN'
                }
            
            # Train and evaluate SVM if selected
            if args.classifier in ['svm', 'all']:
                svm_output_dir = os.path.join(output_dir, f'svm_{method}')
                os.makedirs(svm_output_dir, exist_ok=True)
                
                print("\n" + "="*60)
                print(f"SVM CLASSIFICATION WITH {method_name} DIMENSIONALITY REDUCTION")
                print(f"Number of features: {data['n_components']}")
                print("="*60)
                
                # Create SVM model
                svm = SVMClassifier(output_dir=svm_output_dir)
                
                # Train SVM with selected strategy
                if args.svm_strategy == 'standard':
                    # Simple grid search for standard SVM
                    svm.train_grid_search(data['train'], y_train, strategy='standard')
                elif args.svm_strategy == 'ovr':
                    # One-vs-Rest strategy
                    svm.train_grid_search(data['train'], y_train, strategy='ovr')
                elif args.svm_strategy == 'ovo':
                    # One-vs-One strategy
                    svm.train_grid_search(data['train'], y_train, strategy='ovo')
                elif args.svm_strategy == 'ensemble':
                    # Ensemble of SVMs with different kernels
                    svm.train_ensemble(data['train'], y_train, voting='soft')
                
                # Evaluate SVM model
                svm_accuracy, _ = svm.evaluate(data['test'], y_test, rock_classes, f'_svm_{method}')
                
                # Save model
                svm.save_model(f'svm_model_{method}.pkl')
                
                results[f'svm_{method}'] = {
                    'accuracy': svm_accuracy,
                    'name': f'SVM ({args.svm_strategy}) with {method_name}',
                    'n_components': data['n_components'],
                    'classifier': 'SVM'
                }
    
    # Train and evaluate CNN if selected
    if is_cnn:
        cnn_output_dir = os.path.join(output_dir, 'cnn')
        os.makedirs(cnn_output_dir, exist_ok=True)
        
        print("\n" + "="*60)
        print(f"CNN CLASSIFICATION")
        print("="*60)
        
        # Load image paths for CNN
        print("\nLoading image data for CNN...")
        train_images, train_labels = load_image_data(train_dir, rock_classes)
        valid_images, valid_labels = load_image_data(valid_dir, rock_classes)
        test_images, test_labels = load_image_data(test_dir, rock_classes)
        
        print(f"Training set: {len(train_images)} images")
        print(f"Validation set: {len(valid_images)} images")
        print(f"Test set: {len(test_images)} images")
        
        # Create CNN model
        cnn = CNNClassifier(output_dir=cnn_output_dir)
        
        # Train CNN model
        if args.cnn_model == 'simple':
            print("\nTraining simple CNN from scratch...")
            cnn.train_simple_cnn(
                train_images, train_labels, 
                valid_images, valid_labels,
                batch_size=args.cnn_batch_size,
                epochs=args.cnn_epochs,
                learning_rate=0.001
            )
        else:
            print(f"\nTraining CNN using transfer learning with {args.cnn_model}...")
            cnn.train_transfer_learning(
                train_images, train_labels,
                valid_images, valid_labels,
                model_name=args.cnn_model,
                batch_size=args.cnn_batch_size,
                epochs=args.cnn_epochs,
                freeze_backbone=args.freeze_backbone
            )
        
        # Evaluate CNN model
        cnn_accuracy, _ = cnn.evaluate(test_images, test_labels, rock_classes)
        
        # Save CNN model
        cnn.save_model(f'cnn_model_{args.cnn_model}.pth')
        
        # Add CNN results
        if 'results' not in locals():
            results = {}
        
        results['cnn'] = {
            'accuracy': cnn_accuracy,
            'name': f'CNN ({args.cnn_model})',
            'n_components': 'N/A',
            'classifier': 'CNN'
        }
    
    # Compare results if multiple methods were used
    if len(results) > 1:
        print("\n" + "="*60)
        print("CLASSIFICATION RESULTS COMPARISON")
        print("="*60)
        
        for model_key, result in results.items():
            print(f"{result['name']}: Accuracy = {result['accuracy']:.4f}")
        
        # Visualize comparison (for non-CNN or all methods)
        if not is_cnn or args.classifier == 'all':
            plt.figure(figsize=(12, 6))
            
            # Group by dimensionality reduction method
            methods = sorted(list(set([key.split('_')[1] for key in results.keys() if '_' in key])))
            classifiers = sorted(list(set([result['classifier'] for result in results.values()])))
            
            bar_width = 0.35
            index = np.arange(len(methods))
            
            for i, classifier in enumerate(classifiers):
                if classifier == 'CNN':
                    continue  # Skip CNN in this graph
                
                accuracies = []
                for method in methods:
                    # Find the result for this classifier and method combination
                    key = f"{classifier.lower()}_{method}"
                    if key in results:
                        accuracies.append(results[key]['accuracy'])
                    else:
                        accuracies.append(0)  # No result for this combination
                
                plt.bar(index + i*bar_width, accuracies, bar_width,
                       label=classifier, alpha=0.8)
            
            plt.xlabel('Dimensionality Reduction Method')
            plt.ylabel('Test Accuracy')
            plt.title('Classification Performance Comparison')
            plt.xticks(index + bar_width/2, [reduction_data[m]['name'] for m in methods])
            plt.legend()
            plt.ylim(0, 1)
            plt.grid(axis='y')
            
            # Add accuracy values on top of bars
            for i, classifier in enumerate(classifiers):
                if classifier == 'CNN':
                    continue
                
                for j, method in enumerate(methods):
                    key = f"{classifier.lower()}_{method}"
                    if key in results:
                        accuracy = results[key]['accuracy']
                        plt.text(j + i*bar_width, accuracy + 0.02, f"{accuracy:.3f}", 
                                ha='center', va='bottom', fontsize=9)
                
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'classification_comparison.png'))
            plt.close()
        
        # Create a separate plot for all classifiers including CNN
        plt.figure(figsize=(10, 6))
        all_models = list(results.keys())
        accuracies = [results[m]['accuracy'] for m in all_models]
        model_names = [results[m]['name'] for m in all_models]
        
        # Plot as bar chart
        plt.bar(range(len(all_models)), accuracies)
        plt.xticks(range(len(all_models)), model_names, rotation=45, ha='right')
        plt.ylim(0, 1)
        plt.xlabel('Model')
        plt.ylabel('Test Accuracy')
        plt.title('All Classifiers Comparison')
        plt.grid(axis='y')
        
        # Add accuracy values on top of bars
        for i, accuracy in enumerate(accuracies):
            plt.text(i, accuracy + 0.02, f"{accuracy:.3f}", ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'all_classifiers_comparison.png'))
        plt.close()
        
        # Save comparison results
        with open(os.path.join(output_dir, 'comparison_results.txt'), 'w') as f:
            f.write(f"Dataset: {data_dir}\n")
            f.write(f"Feature extraction: {'Advanced' if args.advanced_features else 'Basic'}\n\n")
            f.write("RESULTS SUMMARY:\n")
            
            for model_key, result in results.items():
                f.write(f"{result['name']}: Accuracy = {result['accuracy']:.4f}\n")
            
            # Find best model
            best_model = max(results.items(), key=lambda x: x[1]['accuracy'])
            f.write(f"\nBest model: {best_model[1]['name']} with accuracy {best_model[1]['accuracy']:.4f}\n")
    
    print(f"\nAll results saved to {output_dir}")
    print("Experiment completed!")

if __name__ == "__main__":
    main() 