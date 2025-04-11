# Image Classification with Optional Subclassing, Dimension Reduction

This project implements a flexible image classification system with the following features:

1. Dataset loading and validation
2. Optional data augmentation and class balancing
3. Optional dimension reduction (PCA or LDA)
4. Optional subclass clustering before classification
   - Fixed number of subclusters per class
   - Automatic recursive subclass determination
5. Multiple classifiers (KNN, SVM, CNN placeholder, DBSCAN)

## Directory Structure

```
code/
├── classifier/          # Classification algorithms
│   ├── cnn.py           # CNN classifier (placeholder)
│   ├── dbscan.py        # DBSCAN classifier with recursive clustering
│   ├── knn.py           # KNN classifier
│   └── svm.py           # SVM classifier
├── dim_reducer/         # Dimension reduction methods
│   ├── lda.py           # Linear Discriminant Analysis
│   └── pca.py           # Principal Component Analysis
├── utils/               # Utility functions
│   ├── augmentate_dataset.py  # Data augmentation
│   ├── check_dataset.py       # Dataset validation 
│   └── load_dataset.py        # Dataset loading
├── README.md            # This file
├── requirements.txt     # Dependencies
└── train.py             # Main training script
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

The main entry point is `train.py` which takes various command line arguments to configure the training process.

### Basic Usage

```bash
python train.py --data_dir ../data
```

### Data Augmentation

```bash
# Basic augmentation (doubles the dataset size)
python train.py --data_dir ../data --augment

# Specify the augmentation factor (creates 3x more data)
python train.py --data_dir ../data --augment --augment_factor 3

# Balance classes using augmentation
python train.py --data_dir ../data --balance_classes
```

### Dimension Reduction

```bash
# Using PCA (retain 95% of variance)
python train.py --data_dir ../data --dim_reducer pca --pca_components 0.95

# Using PCA (specific number of components)
python train.py --data_dir ../data --dim_reducer pca --pca_components 50

# Using LDA (specific number of components)
python train.py --data_dir ../data --dim_reducer lda --lda_components 8

# Using LDA with default components (n_classes-1)
python train.py --data_dir ../data --dim_reducer lda
```

### Subclass Classification

#### Fixed Subclass Clustering

```bash
# KNN with fixed subclass clustering (2 subclusters per class)
python train.py --data_dir ../data --classifier knn --subclass --n_subclusters 2

# SVM with fixed subclass clustering (3 subclusters per class)
python train.py --data_dir ../data --classifier svm --kernel rbf --subclass --n_subclusters 3
```

#### Recursive Automatic Subclass Clustering

```bash
# Use recursive clustering with 2 levels of hierarchy
python train.py --data_dir ../data --recursive_subclass --n_subclass_levels 2

# Adjust minimum samples per cluster (affects cluster size)
python train.py --data_dir ../data --recursive_subclass --min_samples 10

# Use DBSCAN classifier directly
python train.py --data_dir ../data --classifier dbscan
```

### Image Preprocessing

```bash
# Resize images to 128x128
python train.py --data_dir ../data --img_size 128 128

# Convert images to grayscale
python train.py --data_dir ../data --grayscale
```

### Full Example

```bash
# Example with fixed subclass clustering and PCA
python train.py --data_dir ../data --img_size 224 224 --grayscale --augment --balance_classes --dim_reducer pca --pca_components 0.95 --classifier svm --kernel rbf --subclass --n_subclusters 3

# Example with recursive subclass clustering and LDA
python train.py --data_dir ../data --img_size 224 224 --grayscale --augment --balance_classes --dim_reducer lda --lda_components 8 --recursive_subclass --n_subclass_levels 3 --min_samples 5
```

## Command Line Arguments

- `--data_dir`: Path to dataset directory
- `--img_size`: Image size (width, height)
- `--grayscale`: Convert images to grayscale

#### Data Augmentation Options
- `--augment`: Use data augmentation
- `--augment_factor`: Number of augmented samples to create per original sample (default=2)
- `--balance_classes`: Balance classes using augmentation

#### Dimension Reduction Options
- `--dim_reducer`: Dimension reduction method (none, pca, lda)
- `--pca_components`: Number of components or variance ratio for PCA (default=0.95)
- `--lda_components`: Number of components for LDA (default=n_classes-1)

#### Classification Options
- `--classifier`: Classifier type (knn, svm, cnn, dbscan)
- `--n_neighbors`: Number of neighbors for KNN classifier
- `--kernel`: Kernel type for SVM classifier

#### Subclass Options
- `--subclass`: Use fixed subclass classification
- `--recursive_subclass`: Use recursive subclass classification with automatic determination
- `--n_subclusters`: Number of subclusters per class (for fixed subclass mode)
- `--n_subclass_levels`: Number of recursive levels for subclass clustering (default=2)
- `--min_samples`: Minimum samples per cluster for DBSCAN (default=5)
