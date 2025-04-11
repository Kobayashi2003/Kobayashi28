# Hierarchical Rock Classification System

This project implements a hierarchical rock classification system using various machine learning techniques. The system first divides each rock type into clusters, and then trains classifiers to predict both rock types and their subclasses.

## Features

- Support for multiple classifier types (KNN, SVM, CNN)
- Dimensionality reduction techniques (PCA, LDA)
- Feature extraction for rock images
- Evaluation tools including confusion matrices and classification reports
- Hyperparameter optimization via grid search

## Installation

1. Clone the repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The main script provides a command-line interface with various options:

```bash
python code/main.py --classifier knn --dim-reduction pca --pca-components 50 --data-path path/to/data --rock-types igneous sedimentary metamorphic
```

### Common Options

- `--classifier`: Type of classifier to use (`knn`, `svm`, or `cnn`)
- `--data-path`: Path to the dataset
- `--rock-types`: List of rock types to classify
- `--dim-reduction`: Dimensionality reduction technique (`pca`, `lda`, or `none`)
- `--pca-components`: Number of PCA components (if using PCA)
- `--lda-components`: Number of LDA components (if using LDA)
- `--subclasses`: Number of subclasses per rock type
- `--output-dir`: Directory to save results
- `--advanced-features`: Enable advanced feature extraction

### KNN-specific Options

For KNN classifier:
```bash
python code/main.py --classifier knn --n-neighbors 5 --weights uniform --algorithm auto --p 2
```

### SVM-specific Options

For SVM classifier:
```bash
python code/main.py --classifier svm --kernel rbf --C 1.0 --gamma scale
```

### CNN-specific Options

For CNN classifier:
```bash
python code/main.py --classifier cnn --model-name resnet50 --batch-size 32 --epochs 10 --learning-rate 0.001
```

## Examples

1. Basic KNN classification:
```bash
python code/main.py --classifier knn --data-path data/rocks
```

2. SVM with grid search:
```bash
python code/main.py --classifier svm --grid-search --data-path data/rocks
```

3. CNN with transfer learning:
```bash
python code/main.py --classifier cnn --model-name resnet50 --freeze-backbone --data-path data/rocks
```

4. Hierarchical classification with PCA:
```bash
python code/main.py --classifier knn --dim-reduction pca --subclasses 3 --data-path data/rocks
```

## Library Usage

You can also use the classifiers programmatically:

```python
from classifier.knn import KNNClassifier
from classifier.svm import SVMClassifier
from classifier.cnn import CNNClassifier

# KNN Example
knn = KNNClassifier(output_dir='./output/knn')
knn.train_standard(X_train, y_train, X_valid, y_valid, n_neighbors=5)
accuracy = knn.evaluate(X_test, y_test, class_names)

# SVM Example
svm = SVMClassifier(output_dir='./output/svm')
svm.train_grid_search(X_train, y_train)
accuracy = svm.evaluate(X_test, y_test, class_names)

# CNN Example
cnn = CNNClassifier(output_dir='./output/cnn')
cnn.train(train_paths, train_labels, valid_paths, valid_labels, class_names, model_name='resnet50')
accuracy = cnn.evaluate(test_paths, test_labels, class_names)
``` 