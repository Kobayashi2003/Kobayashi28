# Standard library imports
import os

# Third-party imports - data analysis and scientific computing
import numpy as np

# Third-party imports - image processing
import cv2
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops

# Third-party imports - machine learning
from sklearn.preprocessing import StandardScaler

# Third-party imports - utilities
from tqdm import tqdm

def load_data(data_dir, classes, feature_extractor=None):
    """
    Load data from directory and extract features
    
    Parameters:
    -----------
    data_dir : str
        Directory containing class subdirectories
    classes : list
        List of class names (subdirectory names)
    feature_extractor : callable, optional
        Function to extract features from images
        
    Returns:
    --------
    features : ndarray
        Extracted features
    labels : ndarray
        Class labels
    """
    features = []
    labels = []
    
    if not os.path.exists(data_dir):
        print(f"Warning: Data directory does not exist: {data_dir}")
        return np.array(features), np.array(labels)
    
    for class_idx, class_name in enumerate(classes):
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.isdir(class_dir):
            print(f"Warning: Class directory does not exist: {class_dir}")
            continue
            
        print(f"Processing class '{class_name}'...")
        img_count = 0
        error_count = 0
            
        for img_name in os.listdir(class_dir):
            if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            img_path = os.path.join(class_dir, img_name)
            
            # Extract features if a feature extractor is provided
            if feature_extractor:
                try:
                    # Read image
                    img = cv2.imread(img_path)
                    if img is None:
                        print(f"Cannot read image: {img_path}")
                        error_count += 1
                        continue
                        
                    # Extract features
                    feat = feature_extractor(img)
                    if feat is not None:
                        features.append(feat)
                        labels.append(class_idx)
                        img_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    print(f"Error processing image {img_path}: {str(e)}")
                    error_count += 1
            else:
                # Just store the image path for later use (useful for CNN)
                # Check if image can be read correctly
                try:
                    img = cv2.imread(img_path)
                    if img is not None:
                        features.append(img_path)
                        labels.append(class_idx)
                        img_count += 1
                    else:
                        print(f"Cannot read image: {img_path}")
                        error_count += 1
                except Exception as e:
                    print(f"Error processing image {img_path}: {str(e)}")
                    error_count += 1
        
        print(f"  Successfully processed: {img_count} images, Errors: {error_count} images")
    
    if len(features) == 0:
        raise ValueError("No images were successfully loaded! Check the data path and image formats.")
        
    return np.array(features), np.array(labels)

def load_image_data(data_dir, classes):
    """
    Load raw image data without feature extraction (for CNN)
    
    Parameters:
    -----------
    data_dir : str
        Directory containing class subdirectories
    classes : list
        List of class names (subdirectory names)
        
    Returns:
    --------
    images : list
        List of image paths
    labels : ndarray
        Class labels
    """
    images = []
    labels = []
    
    for class_idx, class_name in enumerate(classes):
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.isdir(class_dir):
            continue
            
        for img_name in os.listdir(class_dir):
            if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            img_path = os.path.join(class_dir, img_name)
            images.append(img_path)
            labels.append(class_idx)
    
    return images, np.array(labels)

def extract_basic_features(img):
    """
    Extract basic color histogram features from image
    
    Parameters:
    -----------
    img : ndarray
        Image data (already loaded)
        
    Returns:
    --------
    features : ndarray
        Extracted color histogram features
    """
    try:
        # Resize image for consistency
        image_size = (128, 128)
        img_resized = cv2.resize(img, image_size)
        
        # Extract color histograms
        hist_b = cv2.calcHist([img_resized], [0], None, [32], [0, 256])
        hist_g = cv2.calcHist([img_resized], [1], None, [32], [0, 256])
        hist_r = cv2.calcHist([img_resized], [2], None, [32], [0, 256])
        
        # Normalize histograms
        hist_b = cv2.normalize(hist_b, hist_b).flatten()
        hist_g = cv2.normalize(hist_g, hist_g).flatten()
        hist_r = cv2.normalize(hist_r, hist_r).flatten()
        
        # Combine features
        features = np.concatenate([hist_b, hist_g, hist_r])
        
        return features
    except Exception as e:
        print(f"Basic feature extraction error: {str(e)}")
        return None

def extract_advanced_features(img):
    """
    Extract advanced features including color, texture, and shape
    
    Parameters:
    -----------
    img : ndarray
        Image data (already loaded)
        
    Returns:
    --------
    features : ndarray
        Extracted features
    """
    try:
        # Resize image for consistency
        image_size = (128, 128)
        img = cv2.resize(img, image_size)
        
        # Convert to different color spaces
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # 1. Color features
        # Color histograms (BGR)
        hist_b = cv2.calcHist([img], [0], None, [32], [0, 256])
        hist_g = cv2.calcHist([img], [1], None, [32], [0, 256])
        hist_r = cv2.calcHist([img], [2], None, [32], [0, 256])
        
        # HSV histograms
        hist_h = cv2.calcHist([img_hsv], [0], None, [32], [0, 180])
        hist_s = cv2.calcHist([img_hsv], [1], None, [32], [0, 256])
        hist_v = cv2.calcHist([img_hsv], [2], None, [32], [0, 256])
        
        # Normalize histograms
        hist_b = cv2.normalize(hist_b, hist_b).flatten()
        hist_g = cv2.normalize(hist_g, hist_g).flatten()
        hist_r = cv2.normalize(hist_r, hist_r).flatten()
        hist_h = cv2.normalize(hist_h, hist_h).flatten()
        hist_s = cv2.normalize(hist_s, hist_s).flatten()
        hist_v = cv2.normalize(hist_v, hist_v).flatten()
        
        # 2. Texture features
        # Local Binary Pattern
        radius = 3
        n_points = 8 * radius
        lbp = local_binary_pattern(img_gray, n_points, radius, method='uniform')
        lbp_hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, n_points + 3), 
                                 range=(0, n_points + 2))
        lbp_hist = lbp_hist.astype(float)
        lbp_hist /= (lbp_hist.sum() + 1e-6)  # Normalize
        
        # GLCM (Gray-Level Co-Occurrence Matrix) features
        distances = [1]
        angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        glcm = graycomatrix(img_gray, distances, angles, 256, symmetric=True, normed=True)
        
        # Extract properties from GLCM
        contrast = graycoprops(glcm, 'contrast').flatten()
        dissimilarity = graycoprops(glcm, 'dissimilarity').flatten()
        homogeneity = graycoprops(glcm, 'homogeneity').flatten()
        energy = graycoprops(glcm, 'energy').flatten()
        correlation = graycoprops(glcm, 'correlation').flatten()
        
        # 3. Shape features
        # Edge detection
        edges = cv2.Canny(img_gray, 100, 200)
        edge_ratio = np.sum(edges > 0) / (image_size[0] * image_size[1])
        
        # Calculate moments
        moments = cv2.moments(img_gray)
        hu_moments = cv2.HuMoments(moments).flatten()
        
        # Combine all features
        features = np.concatenate([
            hist_b, hist_g, hist_r,
            hist_h, hist_s, hist_v,
            lbp_hist,
            contrast, dissimilarity, homogeneity, energy, correlation,
            np.array([edge_ratio]),
            hu_moments
        ])
        
        # Handle NaN values
        features = np.nan_to_num(features)
        
        return features
    except Exception as e:
        print(f"Advanced feature extraction error: {str(e)}")
        return None

def standardize_features(X_train, X_valid=None, X_test=None):
    """
    Standardize features to zero mean and unit variance
    
    Parameters:
    -----------
    X_train : ndarray
        Training features
    X_valid : ndarray, optional
        Validation features
    X_test : ndarray, optional
        Test features
        
    Returns:
    --------
    standardized_data : tuple
        Tuple of standardized features (X_train_scaled, X_valid_scaled, X_test_scaled)
    scaler : StandardScaler
        Fitted scaler
    """
    # Initialize scaler
    scaler = StandardScaler()
    
    # Fit on training data and transform
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Transform validation and test data if provided
    result = [X_train_scaled]
    
    if X_valid is not None:
        X_valid_scaled = scaler.transform(X_valid)
        result.append(X_valid_scaled)
    
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
        result.append(X_test_scaled)
    
    return tuple(result), scaler
