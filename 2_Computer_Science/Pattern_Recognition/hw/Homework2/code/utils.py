import numpy as np
from scipy import io

def load_data(file_path, train_split=9):
    """
    Load Yale dataset and split into training and test sets
    
    Parameters:
    -----------
    file_path : str
        Path to the .mat file containing the dataset
    train_split : int, default=9
        Number of samples per class to use for training
        
    Returns:
    --------
    X_train : array-like, shape (n_train_samples, n_features)
        Training data
    y_train : array-like, shape (n_train_samples,)
        Training labels
    X_test : array-like, shape (n_test_samples, n_features)
        Test data
    y_test : array-like, shape (n_test_samples,)
        Test labels
    """
    # Load data from .mat file
    data = io.loadmat(file_path)
    fea = data['fea']  # Feature matrix (n_samples, n_features)
    gnd = data['gnd'].flatten()  # Label vector

    # Split data by class
    classes = np.unique(gnd)
    train_data, test_data = [], []
    train_label, test_label = [], []
    
    for c in classes:
        # Get indices of samples of the current class
        indices = np.where(gnd == c)[0]
        # Split into training and test sets
        train_indices = indices[:train_split]
        test_indices = indices[train_split:]
        
        # Append to training and test data and labels
        train_data.append(fea[train_indices])
        test_data.append(fea[test_indices])
        train_label.extend([c] * len(train_indices))
        test_label.extend([c] * len(test_indices))
    
    return (np.vstack(train_data), np.array(train_label),
            np.vstack(test_data), np.array(test_label)) 