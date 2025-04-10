# Rock Image Classification

A modular implementation of rock image classification using KNN with optional dimensionality reduction (PCA and LDA).

## Project Structure

The project is organized into several Python modules with specific responsibilities:

- `data_utils.py`: Data loading, preprocessing, and feature extraction
- `pca.py`: PCA implementation for dimensionality reduction
- `lda.py`: LDA implementation for dimensionality reduction
- `knn.py`: KNN classifier implementation
- `main.py`: Main program that orchestrates the entire workflow

## Prerequisites

```
numpy
matplotlib
opencv-python
scikit-learn
scikit-image
tqdm
joblib
```

You can install all requirements with:

```
pip install -r requirements.txt
```

## Dataset Structure

The dataset should be organized as follows:

```
RockData/
├── train/
│   ├── class1/
│   ├── class2/
│   └── ...
├── valid/
│   ├── class1/
│   ├── class2/
│   └── ...
└── test/
    ├── class1/
    ├── class2/
    └── ...
```

Each class directory should contain images of rocks of that class.

## Usage

Run the main script with various options:

```
python main.py [options]
```

### Command Line Options

- `--data-dir PATH`: Path to the dataset directory (default: ./RockData)
- `--use-augmented`: Use augmented dataset if available
- `--advanced-features`: Use advanced feature extraction (texture, color, shape)
- `--dim-reduction {none,pca,lda,both}`: Dimensionality reduction method to use (default: none)
- `--pca-components N`: Number of PCA components to use (default: auto-determined)
- `--lda-components N`: Number of LDA components to use (default: auto-determined)
- `--output-dir PATH`: Output directory for results (default: ./output)

### Examples

1. Basic KNN with no dimensionality reduction:
```
python main.py
```

2. Use advanced features with PCA dimensionality reduction:
```
python main.py --advanced-features --dim-reduction pca
```

3. Use LDA dimensionality reduction with 5 components:
```
python main.py --dim-reduction lda --lda-components 5
```

4. Compare both PCA and LDA with advanced features:
```
python main.py --advanced-features --dim-reduction both
```

5. Full pipeline with augmented data and all dimensionality reduction methods:
```
python main.py --use-augmented --advanced-features --dim-reduction both
```

## Output

The results are saved in the specified output directory with a timestamp. For each run, the following outputs are generated:

- Classification reports
- Confusion matrices
- Performance visualizations
- Trained models
- Dimensionality reduction visualizations (if PCA or LDA is used)
- Method comparison results (if multiple dimensionality reduction methods are used)

## Implementation Details

### Feature Extraction
- **Basic**: Color histograms
- **Advanced**: Color histograms + LBP texture features + GLCM texture features + shape features

### Dimensionality Reduction
- **PCA**: Principal Component Analysis for unsupervised dimensionality reduction
- **LDA**: Linear Discriminant Analysis for supervised dimensionality reduction

### Classification
- **KNN**: k-Nearest Neighbors with distance weighting 