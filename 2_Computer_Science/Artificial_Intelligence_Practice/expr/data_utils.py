import os
import numpy as np
import cv2
from tqdm import tqdm
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops
from sklearn.preprocessing import StandardScaler

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
    
    for class_idx, class_name in enumerate(classes):
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.isdir(class_dir):
            print(f"警告: 类别目录不存在: {class_dir}")
            continue
            
        print(f"处理类别 '{class_name}'...")
        img_count = 0
        error_count = 0
            
        for img_name in os.listdir(class_dir):
            if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            img_path = os.path.join(class_dir, img_name)
            
            # Extract features if a feature extractor is provided
            if feature_extractor:
                try:
                    # 先读取图像
                    img = cv2.imread(img_path)
                    if img is None:
                        print(f"无法读取图像: {img_path}")
                        error_count += 1
                        continue
                        
                    # 提取特征
                    feat = feature_extractor(img)
                    if feat is not None:
                        features.append(feat)
                        labels.append(class_idx)
                        img_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    print(f"处理图像时出错 {img_path}: {str(e)}")
                    error_count += 1
            else:
                # Just store the image path for later use (useful for CNN)
                # 检查图像是否能够被正确读取
                try:
                    img = cv2.imread(img_path)
                    if img is not None:
                        features.append(img_path)
                        labels.append(class_idx)
                        img_count += 1
                    else:
                        print(f"无法读取图像: {img_path}")
                        error_count += 1
                except Exception as e:
                    print(f"处理图像时出错 {img_path}: {str(e)}")
                    error_count += 1
        
        print(f"  成功处理: {img_count} 图像, 错误: {error_count} 图像")
    
    if len(features) == 0:
        raise ValueError("没有成功加载任何图像！请检查数据路径和图像格式。")
        
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
        # 调整图像大小以确保一致性
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
        print(f"基础特征提取错误: {str(e)}")
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
        # 调整图像大小以确保一致性
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
        
        # Color moments (mean, std, skewness)
        means = np.mean(img, axis=(0, 1))
        stds = np.std(img, axis=(0, 1))
        skewness = np.mean(((img - means) / (stds + 1e-8)) ** 3, axis=(0, 1))
        
        # 2. Texture features
        # Resize for GLCM calculation (for speed)
        img_gray_resized = cv2.resize(img_gray, (100, 100))
        
        # GLCM (Gray Level Co-occurrence Matrix)
        distances = [1, 3]
        angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        glcm = graycomatrix(img_gray_resized, distances, angles, 256, symmetric=True, normed=True)
        
        # GLCM properties
        contrast = graycoprops(glcm, 'contrast').flatten()
        dissimilarity = graycoprops(glcm, 'dissimilarity').flatten()
        homogeneity = graycoprops(glcm, 'homogeneity').flatten()
        energy = graycoprops(glcm, 'energy').flatten()
        correlation = graycoprops(glcm, 'correlation').flatten()
        
        # 3. Shape features
        # Edge detection
        edges = cv2.Canny(img_gray, 100, 200)
        num_edges = np.sum(edges > 0)
        edge_density = num_edges / (edges.shape[0] * edges.shape[1])
        
        # Basic shape metrics
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Sort contours by area and get the largest one
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]  # Consider top 5 contours
            
            contour_areas = np.array([cv2.contourArea(cnt) for cnt in contours])
            contour_perimeters = np.array([cv2.arcLength(cnt, True) for cnt in contours])
            
            # Calculate circularity: 4*pi*area/perimeter^2 (1 for perfect circle)
            with np.errstate(divide='ignore', invalid='ignore'):
                circularities = 4 * np.pi * contour_areas / (contour_perimeters**2)
            circularities = np.nan_to_num(circularities)  # Replace NaN with 0
            
            # Mean and max circularity
            mean_circularity = np.mean(circularities)
            max_circularity = np.max(circularities)
            
            # Contour features
            shape_features = np.array([
                contour_areas.mean(), 
                contour_areas.std() if len(contour_areas) > 1 else 0,
                contour_perimeters.mean(),
                mean_circularity,
                max_circularity,
                len(contours),
                edge_density
            ])
        else:
            # If no contours found, set default values
            shape_features = np.zeros(7)
        
        # Combine all features
        features = np.concatenate([
            hist_b, hist_g, hist_r,  # BGR color histograms
            hist_h, hist_s, hist_v,  # HSV color histograms
            means, stds, skewness,   # Color moments
            contrast, dissimilarity, homogeneity, energy, correlation,  # Texture
            shape_features  # Shape
        ])
        
        return features
    
    except Exception as e:
        print(f"高级特征提取错误: {str(e)}")
        return None

def standardize_features(X_train, X_valid=None, X_test=None):
    """
    Standardize features using training set statistics
    
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
    (X_train_scaled, X_valid_scaled, X_test_scaled) : tuple
        Standardized features
    scaler : StandardScaler
        Fitted scaler
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    result = [X_train_scaled]
    
    if X_valid is not None:
        X_valid_scaled = scaler.transform(X_valid)
        result.append(X_valid_scaled)
    else:
        result.append(None)
        
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
        result.append(X_test_scaled)
    else:
        result.append(None)
        
    return tuple(result), scaler 